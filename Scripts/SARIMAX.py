import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error

# Vorverarbeitung und filtern
df_goldpreis_alles = pd.read_csv('../Data/combined_gold_economic_factors_withweekdays.csv', index_col=0,
                                 parse_dates=True)  # einlesen
df_goldpreis_alles.index = pd.to_datetime(df_goldpreis_alles.index)  #Datum umwandeln
df_goldpreis_alles = df_goldpreis_alles[df_goldpreis_alles.index > pd.Timestamp('2021-01-01')]  # nach 2021 filtern

# Vorverarbeitung für df_goldpreis
df_goldpreis_alles = df_goldpreis_alles.sort_index()
df_goldpreis_alles = df_goldpreis_alles.asfreq('B')
df_goldpreis_alles = df_goldpreis_alles.interpolate(method='linear')
df_goldpreis_alles.index.freq = 'B'


# Aufteilen in Trainingsdaten und Testdaten
train_size = int(0.8 * len(df_goldpreis_alles))
train, test = df_goldpreis_alles[:train_size], df_goldpreis_alles[train_size:]

train_exog = train.drop(columns=['Goldpreis', 'Wochentag'])

model = SARIMAX(
    train['Goldpreis'],
    exog=train_exog,
    order=(1, 1, 1),
    seasonal_order=(0, 0, 0, 0)
)

result = model.fit(disp=False)

# Exogene Testdaten vorbereiten (mit denselben Features wie im Training)
exog_test = test.drop(columns=['Goldpreis', 'Wochentag'])

# Vorhersage
SARIMAX_forecast_Goldpreis = result.forecast(steps=len(test), exog=exog_test)

# MSE berechnen
mse_Goldpreis = mean_squared_error(test['Goldpreis'], SARIMAX_forecast_Goldpreis)

# Ergebnisse anzeigen
print(f'MSE für den Goldpreis: {mse_Goldpreis}')

# Plot für die Vorhersage des Goldpreises
plt.figure(figsize=(14, 7))
plt.plot(train['Goldpreis'], color='darkblue', label='Trainingsdaten Goldpreis')
plt.plot(test.index, test['Goldpreis'], color='lightblue', label='Testdaten Goldpreis')
plt.plot(test.index, SARIMAX_forecast_Goldpreis, color='darkblue', linestyle='--', label='Vorhersage Goldpreis')
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('SARIMAX Vorhersage für den Goldpreis')
plt.legend()
plt.show()