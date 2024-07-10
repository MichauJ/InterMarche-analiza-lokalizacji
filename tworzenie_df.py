import pandas as pd
from wojewodztwa import miasta_wojewodztwa
patterns = {
    'adresy': r'(?P<miasto>[\w\s]+) (?P<kod_pocztowy>\d{2}-\d{3}), (?:ul\. )?(?P<ulica>[\w\s]+ \d+)',
    'godziny otwarcia': r'(?P<godziny>\d{1,2}[:\.]\d{2})',
    'godziny zamknięcia':r'-\s*(?P<godziny>\d{1,2}[:\.]\d{2})'
    }

def stworz_df(sklepy: dict) -> pd.DataFrame:
    """
    Funkcja tworzy ramkę danych z utworzonego wcześniej słownika. Wyodrębnia i dodaje jako nowe kolumny godziny otwarcia,
   przypisuje miastom województwa z osobnego słownika.
    """
    df_sklepy = pd.DataFrame(data = 
        {'Adresy' : [sklepy[i]['adres'] for i in list(sklepy.keys()) ],
        'Poniedziałek-Piątek': [sklepy[i]['godziny otwarcia']['Poniedziałek-Piątek']for i in list(sklepy.keys()) ],
        'Sobota': [sklepy[i]['godziny otwarcia']['Sobota']for i in list(sklepy.keys()) ],
        'Niedziela': [sklepy[i]['godziny otwarcia']['Niedziela']for i in list(sklepy.keys()) ] } )

    df_sklepy[['Miasto', 'Kod pocztowy', 'Ulica']] = df_sklepy['Adresy'].str.extract(patterns['adresy'])
    df_sklepy['Otwarcie pn-pt'] = df_sklepy['Poniedziałek-Piątek'].str.extract(patterns['godziny otwarcia'])
    df_sklepy['Zamkniecie pn-pt'] = df_sklepy['Poniedziałek-Piątek'].str.extract(patterns['godziny zamknięcia'])
    df_sklepy['Otwarcie sb'] = df_sklepy['Sobota'].str.extract(patterns['godziny otwarcia'])
    df_sklepy['Zamkniecie sb'] = df_sklepy['Sobota'].str.extract(patterns['godziny zamknięcia'])
    df_sklepy['Otwarcie nd'] = df_sklepy['Niedziela'].str.extract(patterns['godziny otwarcia'])
    df_sklepy['Zamkniecie nd'] = df_sklepy['Niedziela'].str.extract(patterns['godziny zamknięcia'])
    df_sklepy['Województwo'] = df_sklepy['Miasto'].map(miasta_wojewodztwa)
    df_sklepy.drop(columns=['Poniedziałek-Piątek', 'Sobota','Niedziela'], inplace=True)
    df_sklepy.dropna(subset='Miasto')
    return df_sklepy