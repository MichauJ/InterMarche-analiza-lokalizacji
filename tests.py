#importy
import os
import sys
print("Current working directory:", os.getcwd())
print("Python path:", sys.path)
# Dodaj katalog główny projektu do ścieżki wyszukiwania
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print("Updated Python path:", sys.path)
import unittest
import requests as r
import re
import unittest
from unittest.mock import patch, mock_open, MagicMock
from bs4 import BeautifulSoup
import os
from tworzenie_df import patterns
import pandas as pd
from pandas.testing import assert_frame_equal
from wojewodztwa import miasta_wojewodztwa

#################################################################################

class TestPobierzDaneZHtml(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open)
    @patch('requests.get')
    def test_pobierz_dane_z_html(self, mock_get, mock_file):
        from pobranie_url import pobierz_dane_z_url
        # Mockowanie odpowiedzi requests
        mock_response = MagicMock()
        mock_response.text = '<html><body><h1>Test</h1></body></html>'
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        # Stwórz katalog "Dane", jeśli nie istnieje
        if not os.path.exists('Dane'):
            os.mkdir('Dane')
        # Wywołaj funkcję z określonym URL i nazwą pliku
        output_filename = 'Sklepy_Intermarche_raw.html'
        pobierz_dane_z_url('http://example.com', output_filename)
        # Sprawdzenie, czy requests.get zostało wywołane z odpowiednim URL
        mock_get.assert_called_once_with('http://example.com')
        # Sprawdzenie, czy plik został otwarty w trybie zapisu z odpowiednią nazwą
        expected_path = os.path.join(os.getcwd(), 'Dane', output_filename)
        mock_file.assert_called_once_with(expected_path, 'x', encoding='utf-8')
        
        # Sprawdzenie, czy zawartość została zapisana do pliku
        handle = mock_file()
        handle.write.assert_called_once_with('<html><body><h1>Test</h1></body></html>')
class TestWczytajIOczyscHtml(unittest.TestCase):
    def test_wczytaj_i_oczysc_html(self):
        # Przykładowy HTML do testowania
        html_content = '''
        <div class="market__address">Aleksandrów Łódzki 95-070 , ul. Senatorska 4</div>
        <div class="market__information">Pn-Pt 08:00 - 20:00<br>Sb 08:00 - 18:00<br>Niedziela handlowa 10:00 - 16:00</div>
        <div class="market__address">Warszawa 00-001 , ul. Nowa 1</div>
        <div class="market__information">Pn-Pt 09:00 - 21:00<br>Sb 09:00 - 19:00<br>Niedziela handlowa 11:00 - 17:00</div>
        '''

        # Mockowanie otwarcia pliku
        mock_path = 'mocked_file.html'
        with patch('builtins.open', mock_open(read_data=html_content)):
            from pobranie_url import wczytaj_i_oczysc_html  # Zmiana 'your_module' na nazwę właściwego modułu
            
            # Wywołanie testowanej funkcji
            result = wczytaj_i_oczysc_html(mock_path)
            
            # Oczekiwany wynik
            expected_result = {
                0: {
                    'adres': 'Aleksandrów Łódzki 95-070 , ul. Senatorska 4',
                    'godziny otwarcia': {
                        'Poniedziałek-Piątek': 'Pn-Pt 08:00 - 20:00',
                        'Sobota': 'Sb 08:00 - 18:00',
                        'Niedziela': 'Niedziela handlowa 10:00 - 16:00'
                    }
                },
                1: {
                    'adres': 'Warszawa 00-001 , ul. Nowa 1',
                    'godziny otwarcia': {
                        'Poniedziałek-Piątek': 'Pn-Pt 09:00 - 21:00',
                        'Sobota': 'Sb 09:00 - 19:00',
                        'Niedziela': 'Niedziela handlowa 11:00 - 17:00'
                    }
                }
            }
            
            # Sprawdzenie, czy wynik jest zgodny z oczekiwanym
            self.assertEqual(result, expected_result)      
class TestZnajdowanieAdresow(unittest.TestCase):
    test_cases = [
        'Głuchołazy 48-340, ul.Grunwaldzka 2 b',
        'Gdynia Pogórze 81-198, ul. Płk. Dąbka 338 (Galeria Szperk)',
        'Gostyń 63-800, os. 700-lecia 16',
        'Gryfino 74-100, ul. 9.Maja 14'
    ]
    expected_result = ['Głuchołazy', 'Gdynia Pogórze', 'Gostyń', 'Gryfino']
    wzor_miasto = patterns['miasto']

    def test_wzoru_miasta(self):
        test_result = []
        for case in self.test_cases:
            wynik = re.findall(self.wzor_miasto, case)[0].strip()
            test_result.append(wynik)
        self.assertEqual(test_result, self.expected_result)
    


if __name__ == '__main__':
    unittest.main()