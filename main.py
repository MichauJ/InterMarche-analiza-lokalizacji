from ast import If
import os
from string import printable
from pobranie_url import pobierz_dane_z_url,wczytaj_i_oczysc_html
from tworzenie_df import stworz_df, patterns
from wojewodztwa import miasta_wojewodztwa
# Pobierz dane - done
if os.path.isfile(os.getcwd()+'/Dane/Strona html z listą sklepów Intermarche.html') == False:
    pobierz_dane_z_url(
         'https://intermarche.pl/o-nas/nasze-sklepy/#',
         output_filename='Strona html z listą sklepów Intermarche.html'
         )

sklepy = wczytaj_i_oczysc_html(os.getcwd()+'/Dane/Strona html z listą sklepów Intermarche.html')
df = stworz_df(sklepy)
df.to_excel(os.getcwd()+'/Dane/'+'Sklepy Intermarche.xlsx')

