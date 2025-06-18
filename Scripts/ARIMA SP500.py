import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima.model import ARIMA

# Vorverarbeitung und filtern
df_goldpreis_alles=pd.read_csv('../Data/combined_gold_economic_factors_withweekdays.csv', index_col=0, parse_dates=True) # einlesen
df_goldpreis_alles.index = pd.to_datetime(df_goldpreis_alles.index) #Datum umwandeln
df_goldpreis_alles = df_goldpreis_alles[df_goldpreis_alles.index > pd.Timestamp('2021-01-01')] # nach 2021 filtern

# Vorverarbeitung
df_SP500 = df_goldpreis_alles['SP500']
df_SP500 = df_SP500.sort_index()
df_SP500 = df_SP500.asfreq('B')
df_SP500 = df_SP500.interpolate(method='linear')
df_SP500.index.freq = 'B'

# Aufteilen in Trainingsdaten und Testdaten
train_size = int(0.8 * len(df_SP500))
train, test = df_SP500[:train_size], df_SP500[train_size:]

# ARIMA Modell fitten
arima_model_SP = (ARIMA(train, order=(3, 2, 3)))
arima_model_SP_fit = arima_model_SP.fit()

# Vorhersage für die Testdaten
arima_forecast_SP = arima_model_SP_fit.forecast(steps=len(test))

# MSE berechnen
mse_SP500 = mean_squared_error(test, arima_forecast_SP)

# Ergebnisse anzeigen
print(f'MSE für SP500: {mse_SP500}')

# Plot für die Vorhersage des Goldpreises
plt.figure(figsize=(14, 7))
plt.plot(train, color='darkblue', label='Trainingsdaten')
plt.plot(test.index, test, color='lightblue', label='Testdaten')
plt.plot(test.index, arima_forecast_SP, color='darkblue', linestyle='--', label='Vorhersage Goldpreis')
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('ARIMA Vorhersage SP500')
plt.legend()
plt.show()