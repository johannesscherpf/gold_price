import yfinance as yf
import pandas as pd

# "CL=F" steht für Ölpreis
ticker_symbol = 'CL=F'

# Zeitraum für die Daten
data_period = "10y"  # 1y = 1 Jahr

#download oil data from yahoo finacne api
oil_data = yf.download(ticker_symbol, period=data_period, interval='1d')

# nur closed price holen
oil_close_prices = oil_data[['Close']]

#Speichern
csv_filename = 'oil_prices.csv'
oil_close_prices.to_csv(csv_filename)

print(f"Ölpreise erfolgreich in {csv_filename} gespeichert.")

oil_close_prices.info

