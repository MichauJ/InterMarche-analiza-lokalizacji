from ast import pattern
import pandas as pd
from geopy.geocoders import OpenCage
from geopy.extra.rate_limiter import RateLimiter
import re
from wojewodztwa import miasta_wojewodztwa
from tworzenie_df import df_sklepy
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