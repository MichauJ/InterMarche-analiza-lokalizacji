import enum
from gettext import find
from queue import Empty
from types import NoneType
from bs4 import BeautifulSoup
import re
import requests as r
import os

def pobierz_dane_z_url(url, output_filename='Sklepy_Intermarche_raw.html')-> str:
    """
    Funkcja pobiera dane z url i zapisuje je w pliku html. Zwraca lokalizację utworzonego pliku.
    """
    html = r.get(url)
    print(f"Status:{html} ")
    html_text = html.text
    lokalizacja_pliku_html = os.getcwd()+'\\Dane\\'+output_filename
    os.makedirs('Dane')
    with open(lokalizacja_pliku_html, 'w', encoding= 'utf-8') as html_file:
        html_file.write(html_text)
    print(f'Pobrano stronę html zawierającą listę sklepów InterMarche i zapisano w {lokalizacja_pliku_html}.')
    
def wczytaj_i_oczysc_html(sciezka_do_pliku):
    """
    Funkcja wczytująca plik html i dokonująca jego oczyszczanie.
    """
    with open(sciezka_do_pliku,'r',encoding='utf-8') as html_file: 
        content = html_file.read()
        soup = BeautifulSoup(content,'lxml')
    sklepy = {}
    adresy = soup.find_all('div',class_ = 'market__address')
    godziny_otwarcia = soup.find_all('div',class_ = 'market__information')
    czyszczenie_adresow = '^(<div class="market__address">)|(\s{2,})|(\\n)|$(<p>)'
    czyszczenie_godzin = {
       'Pn-Pt':'Pn-Pt \d{,2}[:\.]\d{2}\s*-\s*\d{,2}[:\.]\d{2}',
       'Sb':'Sb \d{,2}[:\.]\d{2}\s*-\s*\d{,2}[:\.]\d{2}',
       'Nd':'Niedziela handlowa \d{,2}[:\.]\d{2}\s*-\s*\d{,2}[:\.]\d{2}'       
    }
    for i,markety in enumerate(zip(adresy,godziny_otwarcia)):
        sklepy[i] = {'adres':re.sub(czyszczenie_adresow,'',markety[0].text),
                     'godziny otwarcia':{
                           'Poniedziałek-Piątek': 
                                    "NaN" if (match := re.search(czyszczenie_godzin['Pn-Pt'], markety[1].text)) is None else match.group(0),
                           'Sobota': 
                                    "NaN" if (match := re.search(czyszczenie_godzin['Sb'], markety[1].text)) is None else match.group(0),
                           'Niedziela': 
                                    "NaN" if (match := re.search(czyszczenie_godzin['Nd'], markety[1].text)) is None else match.group(0)
                         }
                      }
    return sklepy