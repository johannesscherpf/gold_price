import pandas as pd
from sklearn.metrics import mean_squared_error
import numpy as np

# Laden der tatsächlichen Daten
actual_csv = '../data/XGBoostDaten/Goldpreis.csv'  # Pfad zur CSV-Datei mit den tatsächlichen Goldpreisen
actual_df = pd.read_csv(actual_csv)

# Laden der vorhergesagten Daten
predicted_csv = '../data/XGBoostDaten/gold_price_predictions.csv'  # Pfad zur CSV-Datei mit den vorhergesagten Goldpreisen
predicted_df = pd.read_csv(predicted_csv)

# Sicherstellen, dass das Datum im richtigen Format ist
actual_df['date'] = pd.to_datetime(actual_df['date'])
predicted_df['date'] = pd.to_datetime(predicted_df['date'])

# Sicherstellen, dass die Daten nach Datum sortiert sind
actual_df.sort_values(by='date', ascending=True, inplace=True)
predicted_df.sort_values(by='date', ascending=True, inplace=True)

# Abgleich nach Datum
merged_df = pd.merge(actual_df, predicted_df, on='date', suffixes=('_actual', '_predicted'))

# Überprüfen der tatsächlichen Spaltennamen nach dem Merge
print(merged_df.head())  # Hilft bei der Bestätigung von Spaltennamen

# Berechnung des RMSE
try:
    rmse = np.sqrt(mean_squared_error(merged_df['actual'], merged_df['prediction']))
    print(f'RMSE: {rmse:.2f}')
except KeyError as e:
    print(f"KeyError: {e}. Bitte sicherstellen, dass die Spaltennamen korrekt sind.")