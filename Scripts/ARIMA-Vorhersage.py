import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima.model import ARIMA


# Vorverarbeitung und filtern
df_goldpreis_alles=pd.read_csv('../Data/combined_gold_economic_factors_withweekdays.csv', index_col=0, parse_dates=True) # einlesen
df_goldpreis_alles.index = pd.to_datetime(df_goldpreis_alles.index) #Datum umwandeln
df_goldpreis_alles = df_goldpreis_alles[df_goldpreis_alles.index > pd.Timestamp('2021-01-01')] # nach 2021 filtern
df_goldpreis=df_goldpreis_alles['Goldpreis']

#Vorverarbeitung
df_goldpreis = df_goldpreis.sort_index()
df_goldpreis = df_goldpreis.asfreq('B')
df_goldpreis = df_goldpreis.interpolate(method='linear')
df_goldpreis.index.freq = 'B'


# Aufteilen in Trainingsdaten und Testdaten
train_size = int(0.8 * len(df_goldpreis))
train, test = df_goldpreis[:train_size], df_goldpreis[train_size:]

# ARIMA Modell fitten
arima_model_Goldpreis = ARIMA(train, order=(20, 2, 1))
arima_model_Goldpreis_fit = arima_model_Goldpreis.fit()

# Vorhersage für die Testdaten
arima_forecast_Goldpreis = arima_model_Goldpreis_fit.forecast(steps=len(test))

# MSE berechnen
mse_Goldpreis = mean_squared_error(test, arima_forecast_Goldpreis)

# Ergebnisse anzeigen
print(f'MSE für den Goldpreis: {mse_Goldpreis}')


# Plot für die Vorhersage des Goldpreises
plt.figure(figsize=(14, 7))
plt.plot(train, color='darkblue', label='Trainingsdaten Goldpreis')
plt.plot(test.index, test, color='lightblue', label='Testdaten Goldpreis')
plt.plot(test.index, arima_forecast_Goldpreis, color='darkblue', linestyle='--', label='Vorhersage Goldpreis')
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('ARIMA Vorhersage für den Goldpreis')
plt.legend()
plt.show()

# Vorhersage für die Testdaten
arima_forecast_Goldpreis = arima_model_Goldpreis_fit.forecast(steps=6)

print(arima_forecast_Goldpreis)

# Series in DataFrame umwandeln
forecast_df = arima_forecast_Goldpreis.reset_index()
forecast_df.columns = ['Datum', 'Prognose']

# Speichern als CSV
forecast_df.to_csv('Goldpreis_Vorhersage.csv', index=False)
print("Vorhersage erfolgreich gespeichert.")