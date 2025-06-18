import pandas as pd
import requests

# Dein API-Schlüssel von Alpha Vantage
api_key = 'JX03FK2W87N81TEN'

# API-Endpunkt für den täglichen Goldpreis (XAU/USD)
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=XAUUSD&apikey={api_key}&outputsize=full'

# API-Anfrage senden
response = requests.get(url)
data = response.json()

# Die historischen Daten aus der Antwort extrahieren
if "Time Series (Daily)" in data:
    time_series = data["Time Series (Daily)"]

    # Die Daten in ein pandas DataFrame umwandeln
    df = pd.DataFrame.from_dict(time_series, orient='index')
    df = df.astype(float)  # Umwandeln der Daten in numerische Werte
    df.index = pd.to_datetime(df.index)  # Index als Datum umwandeln

    # Nur die Spalte '4. close' auswählen und umbenennen
    df = df[['4. close']]
    df = df.rename(columns={'4. close': 'Goldpreis'})

    # Die Spalte für den Preis am nächsten Tag erstellen
    df['Goldpreis_gestern'] = df['Goldpreis'].shift(-1)

    # Fehlende Werte am Ende auffüllen
    df = df.dropna()

    # In CSV-Datei speichern
    df.to_csv(r'../data/Goldpreis.csv')
    print('Daten wurden erfolgreich als CSV gespeichert.')

    # Ausgabe der ersten Zeilen des DataFrames
    print(df.head())
    print(len(df))
    print(df.index.min())  # Ältestes Datum
    print(df.index.max())  # Neuestes Datum

else:
    print("Fehlerhafte API-Antwort:")
    print(data)