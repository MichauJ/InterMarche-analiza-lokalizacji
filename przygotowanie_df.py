from ast import pattern
import pandas as pd
from geopy.geocoders import OpenCage
from geopy.extra.rate_limiter import RateLimiter
import re
from wojewodztwa import miasta_wojewodztwa
import pobranie_danych_sklepow
from pobranie_danych_sklepow import df_sklepy

# Ustawienie opcji pandas, aby wyświetlić wszystkie wiersze i kolumny
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Wzorzec do wyodrębnienia miasta, kodu pocztowego i ulicy
# stary: pattern_adresy = r'(?P<miasto>[\w\s]+) (?P<kod_pocztowy>\d{2}-\d{3}), (?:ul\. )?(?P<ulica>[\w\s]+ \d+)'
pattern_adresy = r'(?P<miasto>[\w\.-]+(?:\s[\w\.-]+)*) (?P<kod_pocztowy>\d{2}-\d{3}), (?P<ulica>(?:ul\. |Al\. |os\. |ul\.)?[\w\s\.-]+\d+\s?\w*)'
pattern_godziny_otwarcia = r'(?P<godziny>\d{1,2}[:\.]\d{2})'
pattern_godziny_zamkniecia = r'-\s*(?P<godziny>\d{1,2}[:\.]\d{2})'
# Zastosowanie funkcji str.extract

df_sklepy[['Miasto', 'Kod pocztowy', 'Ulica']] = df_sklepy['Adresy'].str.extract(pattern_adresy)
df_sklepy['Otwarcie pn-pt'] = df_sklepy['Poniedziałek-Piątek'].str.extract(pattern_godziny_otwarcia)
df_sklepy['Zamkniecie pn-pt'] = df_sklepy['Poniedziałek-Piątek'].str.extract(pattern_godziny_zamkniecia)
df_sklepy['Otwarcie sb'] = df_sklepy['Sobota'].str.extract(pattern_godziny_otwarcia)
df_sklepy['Zamkniecie sb'] = df_sklepy['Sobota'].str.extract(pattern_godziny_zamkniecia)
df_sklepy['Otwarcie nd'] = df_sklepy['Niedziela'].str.extract(pattern_godziny_otwarcia)
df_sklepy['Zamkniecie nd'] = df_sklepy['Niedziela'].str.extract(pattern_godziny_zamkniecia)
df_sklepy['Województwo'] = df_sklepy['Miasto'].map(miasta_wojewodztwa)

df_sklepy.drop(columns=['Poniedziałek-Piątek', 'Sobota','Niedziela'], inplace=True)
df_sklepy.dropna(subset='Miasto')



# # Uzyskaj klucz API z OpenCage i zamień 'YOUR_API_KEY' na właściwy klucz
# api_key = 'b73e92835fb642489192a43feb01b312'
# geolocator = OpenCage(api_key)

# # Funkcja do pozyskiwania współrzędnych
# def get_coordinates(city):
#     lokalizacja = geolocator.geocode(city + ", Polska")
#     if lokalizacja:
#         return (lokalizacja.latitude, lokalizacja.longitude)
#     else:
#         return (None, None)

# # Ograniczanie liczby zapytań na sekundę
# geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# # Przypisanie współrzędnych do DataFrame
# df_sklepy['Koordynaty'] = df_sklepy['Miasto'].apply(geocode).apply(lambda loc: (loc.latitude, loc.longitude) if loc else (None, None))
# df_sklepy[['Szerokość', 'Długość']] = pd.DataFrame(df_sklepy['Koordynaty'].tolist(), index=df_sklepy.index)
# df_sklepy.drop(columns=['Koordynaty'], inplace=True)
df_sklepy.to_csv('Sklepy Intermarche.csv',sep=',',encoding='utf-8')
print('Utworzono plik csv!')


print(df_sklepy)