from turtle import color
import numpy as np
import pandas as pd
import plotly.express as px
import os
import matplotlib.pyplot as plt
import seaborn as sns
from wojewodztwa import wojewodztwa_lokalizacje

sns.set_style('white')


lokalizacja_danych = os.getcwd()+'/Dane/'+'Sklepy Intermarche.xlsx'
data = pd.read_excel(lokalizacja_danych)
data2 = data.copy()

# Filter out rows with missing latitude and longitude values
data = data.dropna(subset=['Szerokość', 'Długość'])
# Create a heatmap using Plotly
def heatmap_miasta():
    fig = px.density_mapbox(
        data, 
        lat='Szerokość', 
        lon='Długość',
        hover_name='Miasto',
        radius=10, 
        center=dict(lon=19, lat=52),  # ustawienie centrum na przybliżone centrum Polski
        zoom=5,  # Adjust the zoom level
        mapbox_style="carto-positron",
        opacity=0.6
    )
    # Update the map layout
    fig.update_layout(
        title='Mapa cieplna sklepów Intermarche',
        coloraxis_showscale=True,  # Hide the color scale legend
    )
    # Show the interactive heatmap
    fig.show()
#histogram wojewodzt

def heatmap_wojewodztwa():
    #przygotowanie danych z liczba sklepow w wojewodztwach
    wojewodztwa_counts = data['Województwo'].value_counts()
    # Tworzenie DataFrame na podstawie danych
    df = pd.DataFrame({
        "Wojewodztwo": list(wojewodztwa_counts.index),
        "Liczba sklepow": list(wojewodztwa_counts.values),
        "Szerokość": [wojewodztwa_lokalizacje[wojewodztwo]['lat'] for wojewodztwo in wojewodztwa_counts.index],
        "Długość": [wojewodztwa_lokalizacje[wojewodztwo]['lon'] for wojewodztwo in wojewodztwa_counts.index]
    })
    print(df)
    fig = px.density_mapbox(
        df, 
        lat='Szerokość', 
        lon='Długość',
        z = 'Liczba sklepow',
        radius=60,
        center=dict(lon=19, lat=52),
        hover_data= 'Liczba sklepow',
        hover_name= 'Wojewodztwo',
        zoom=4,
        mapbox_style="carto-positron",
        opacity=1, 
        color_continuous_scale = 'redor'
    )
    # Update the map layout
    fig.update_layout(
        title='Mapa cieplna sklepów Intermarche zgrupowana w województwa',
        coloraxis_showscale=True, 
    )
    # Show the interactive heatmap
    fig.show()


def histogram():
    # obliczenie liczby sklepów w województwach
    wojewodztwa_counts = data['Województwo'].value_counts()
    plt.figure(figsize=(12, 6))
    plt.barh(wojewodztwa_counts.index, wojewodztwa_counts.values, color = 'red')
    for x, y in zip(wojewodztwa_counts.index, wojewodztwa_counts.values):
        plt.text(x=y, y=x, s='{:.0f}'.format(y), color='red')
    plt.title('Liczba sklepów w podziale na województwa')
    plt.gca().invert_yaxis()
    plt.show()
    