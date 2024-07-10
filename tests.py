import unittest
import requests as r
import unittest
from unittest.mock import patch, mock_open, MagicMock
from bs4 import BeautifulSoup
import os
import pandas as pd
from pandas.testing import assert_frame_equal
from wojewodztwa import miasta_wojewodztwa


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
class TestWzorAdresow(unittest.TestCase):
    def test_wyodrebnij_adres(self):
        from tworzenie_df import patterns
        testowe_adresy = [
            'Bolesławiec 59-700, Al. Tysiąclecia 34 a',
            'Brzeg Dolny 56-120, Al. Jerozolimskie31',
            'Czarnków 64-700, ul. Kościuszki 95',
            'Gdańsk 80-337, Al. Grunwaldzka 615',
            'Gryfino 74-100, ul. 9.Maja 14',
            'Nowy Tomyśl 64-300, os. Północ 13'
            ]
        def wyodrebnij_adresy(adresy, pattern):
            extracted_addresses = []
            for adres in adresy:
                match = re.search(pattern, adres)
                if match:
                    extracted_addresses.append(match.groupdict())
            return extracted_addresses

        expected_results = [
            {'miasto': 'Bolesławiec', 'kod_pocztowy': '59-700', 'ulica': 'Al. Tysiąclecia 34'},
            {'miasto': 'Brzeg Dolny', 'kod_pocztowy': '56-120', 'ulica': 'Al. Jerozolimskie 31'},
            {'miasto': 'Czarnków', 'kod_pocztowy': '64-700', 'ulica': 'ul. Kościuszki 95'},
            {'miasto': 'Gdańsk', 'kod_pocztowy': '80-337', 'ulica': 'Al. Grunwaldzka 615'},
            {'miasto': 'Gryfino', 'kod_pocztowy': '74-100', 'ulica': 'ul. 9.Maja 14'},
            {'miasto': 'Nowy Tomyśl', 'kod_pocztowy': '64-300', 'ulica': 'os. Północ 13'}
        ]

        extracted_addresses = wyodrebnij_adresy(testowe_adresy, patterns['adresy'])
        
        self.assertEqual(extracted_addresses, expected_results)
 

if __name__ == '__main__':
    unittest.main()