from ast import If
import os
from string import printable
from pobranie_url import pobierz_dane_z_url,wczytaj_i_oczysc_html
from tworzenie_df import stworz_df, patterns
from wojewodztwa import miasta_wojewodztwa
import pandas as pd

lokalizacja_danych = os.getcwd()+'/Dane/'+'Sklepy Intermarche.xlsx'
lokalizacja_html = os.getcwd()+'/Dane/'+'Strona html z listą sklepów Intermarche.html'
# Pobierz dane
if os.path.isfile(lokalizacja_html) == False:
     pobierz_dane_z_url(
          'https://intermarche.pl/o-nas/nasze-sklepy/#',
          output_filename='Strona html z listą sklepów Intermarche.html'
          )
print('Wczytuję i oczyszczam plik html')
sklepy = wczytaj_i_oczysc_html(lokalizacja_html)
print('Dane oczyszczone, tworze ramkę danych.')
df = stworz_df(sklepy)
try:
    df.to_excel(lokalizacja_danych)
    print(f"Utworzone plik excel w {lokalizacja_danych}.")
except Exception as e:
    print(f'Błąd: {e}')

print('Wizualizacje: ')
#sklepy_df = pd.read_excel(os.getcwd()+'\Dane/'+'Sklepy Intermarche.xlsx')
import wizualizacja as wiz
wiz.heatmap_wojewodztwa()
wiz.heatmap_miasta()
wiz.histogram()


    




