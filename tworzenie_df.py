import pandas as pd
import re
from wojewodztwa import miasta_wojewodztwa
from geopy.geocoders import OpenCage
from geopy.extra.rate_limiter import RateLimiter
patterns = {
    'adresy': r'(?P<miasto>[\w\s]+) (?P<kod_pocztowy>\d{2}-\d{3}), (?:[A-z]{2}\. ) ?(?P<ulica>[\w\s]+ \d+)',
    'miasto': r'[a-zA-ZĄĆĘŁŃÓŚŹŻąćęłńóśźż\s-]+',
    'kod pocztowy': '\d{2}-\d{3}',
    'ulica': r',\s*(.*)$',
    'godziny otwarcia': r'(?P<godziny>\d{1,2}[:\.]\d{2})',
    'godziny zamknięcia':r'-\s*(?P<godziny>\d{1,2}[:\.]\d{2})'
    }

def stworz_df(sklepy: dict) -> pd.DataFrame:
    """
    Funkcja tworzy ramkę danych z utworzonego wcześniej słownika. Wyodrębnia i dodaje jako nowe kolumny godziny otwarcia,
   przypisuje miastom województwa z osobnego słownika. Dodaje też lokalizację miast z geopy 
    """
    df_sklepy = pd.DataFrame(data = 
        {'Adresy' : [sklepy[i]['adres'] for i in list(sklepy.keys()) ],
        'Poniedziałek-Piątek': [sklepy[i]['godziny otwarcia']['Poniedziałek-Piątek']for i in list(sklepy.keys()) ],
        'Sobota': [sklepy[i]['godziny otwarcia']['Sobota']for i in list(sklepy.keys()) ],
        'Niedziela': [sklepy[i]['godziny otwarcia']['Niedziela']for i in list(sklepy.keys()) ] } )
    df_sklepy['Miasto'] = df_sklepy['Adresy'].apply(lambda x: re.findall(patterns['miasto'], x)[0].strip() if re.findall(patterns['miasto'], x) else None)
    df_sklepy['Kod pocztowy'] = df_sklepy['Adresy'].apply(lambda x: re.findall(patterns['kod pocztowy'], x)[0].strip() if re.findall(patterns['kod pocztowy'], x) else None)
    df_sklepy['Ulica'] = df_sklepy['Adresy'].apply(lambda x: re.findall(patterns['ulica'], x)[0].strip() if re.findall(patterns['ulica'], x) else None)
    df_sklepy['Otwarcie pn-pt'] = df_sklepy['Poniedziałek-Piątek'].str.extract(patterns['godziny otwarcia'])
    df_sklepy['Zamkniecie pn-pt'] = df_sklepy['Poniedziałek-Piątek'].str.extract(patterns['godziny zamknięcia'])
    df_sklepy['Otwarcie sb'] = df_sklepy['Sobota'].str.extract(patterns['godziny otwarcia'])
    df_sklepy['Zamkniecie sb'] = df_sklepy['Sobota'].str.extract(patterns['godziny zamknięcia'])
    df_sklepy['Otwarcie nd'] = df_sklepy['Niedziela'].str.extract(patterns['godziny otwarcia'])
    df_sklepy['Zamkniecie nd'] = df_sklepy['Niedziela'].str.extract(patterns['godziny zamknięcia'])
    poprawione_miejscowosci  = {
    'Gdynia Pogórze': 'Gdynia',
    'Jelcz Laskowice': 'Jelcz',
    'Kostrzyn n': 'Kostrzyn nad Odrą',
    'Krynica Zdrój': 'Krynica-Zdrój',
    'Polanica Zdrój': 'Polanica-Zdrój',
    'Swarzędz-Jasin': 'Swarzędz'} #niektóre nazwy są poprawnie łapane przez regex ale niepoprawnie napisane u źródła
    df_sklepy['Miasto'] = df_sklepy['Miasto'].replace(poprawione_miejscowosci)
    df_sklepy['Województwo'] = df_sklepy['Miasto'].map(miasta_wojewodztwa)
    df_sklepy.drop(columns=['Poniedziałek-Piątek', 'Sobota','Niedziela'], inplace=True)
    df_sklepy.dropna(subset='Miasto')

    #dodanie lokalizacji
    from geopy_api_key import api_key
    geolocator = OpenCage(api_key)

    # Funkcja do pozyskiwania współrzędnych
    def get_coordinates(city):
        lokalizacja = geolocator.geocode(city + ", Polska")
        if lokalizacja:
            return (lokalizacja.latitude, lokalizacja.longitude)
        else:
            return (None, None)

    # Ograniczanie liczby zapytań na sekundę
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    # Przypisanie współrzędnych do DataFrame
    df_sklepy['Koordynaty'] = df_sklepy['Miasto'].apply(geocode).apply(lambda loc: (loc.latitude, loc.longitude) if loc else (None, None))
    df_sklepy[['Szerokość', 'Długość']] = pd.DataFrame(df_sklepy['Koordynaty'].tolist(), index=df_sklepy.index)
    df_sklepy.drop(columns=['Koordynaty'], inplace=True)
    
    return df_sklepy