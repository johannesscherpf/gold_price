import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error

# Daten laden und vorbereiten
combined_data = pd.read_csv('../data/combined_gold_economic_factors_withweekdays.csv')
combined_data['Date'] = pd.to_datetime(combined_data['Date'])
combined_data.sort_values(by='Date', ascending=True, inplace=True)

# Merkmale und Zielvariable definieren
features = ['Goldpreis', 'Goldpreis_gestern']
X = combined_data[features]
y = combined_data['Goldpreis']

# Train-Test-Split
train_size = int(len(X) * 0.8)  # Verwenden Sie 80% der Daten für das Training
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# XGBoost-Modelltraining
model = XGBRegressor(objective='reg:squarederror', n_estimators=1000, learning_rate=0.01, max_depth=5)
model.fit(X_train, y_train)

# Vorhersagen auf Testdaten
y_pred_test = model.predict(X_test)

# RMSE Berechnung auf Testdaten
rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
print(f"RMSE auf Testdaten: {rmse:.2f}")

# Visualisierung der Ergebnisse auf den Testdaten
test_date_range = combined_data['Date'][train_size:]

plt.figure(figsize=(14, 7))
plt.plot(test_date_range, y_test, label='Tatsächlicher Preis', color='lightblue')
plt.plot(test_date_range, y_pred_test, label='Vorhergesagter Preis', color='blue', linestyle='dashed')
plt.title('Tatsächlicher vs. Vorhergesagter Goldpreis (Testdaten)')
plt.xlabel('Datum')
plt.ylabel('Goldpreis')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# Vorhersage für die nächsten 10 Tage
last_known_data = X.iloc[-1].copy().values.reshape(1, -1)
future_pred_dates = pd.date_range(start='2025-06-18', periods=10, freq='B')
future_predictions = []

for date in future_pred_dates:
    pred = model.predict(last_known_data)[0]
    future_predictions.append(pred)
    last_known_data = np.array([[pred, last_known_data[0, 0]]])  # Update Goldpreis_gestern mit der neuen Vorhersage

# Zukünftige Vorhersagen ausgeben
prediction_df = pd.DataFrame({
    'date': future_pred_dates,
    'prediction': future_predictions
})
print(prediction_df)

# Speichern der Vorhersagen
prediction_df.to_csv('gold_price_future_predictions.csv', index=False)