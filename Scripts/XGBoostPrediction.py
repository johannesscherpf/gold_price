import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error


combined_data = pd.read_csv('gold_with_features_encoded.csv')
combined_data['Date'] = pd.to_datetime(combined_data['Date'])
combined_data.sort_values(by='Date', ascending=True, inplace=True)

combined_data = combined_data[['Date', 'Goldpreis']]


window_size = 10
lag_size = 5
def create_rolling_features(data, window_size, lag_size):
    features = []
    target = []
    for start in range(len(data) - window_size - lag_size):
        end = start + window_size
        features.append(data.iloc[start:end]['Goldpreis'].values.flatten())
        target.append(data.iloc[end + lag_size]['Goldpreis'])
    return np.array(features), np.array(target)

X, y = create_rolling_features(combined_data, window_size, lag_size)


split_index = len(X) - 10
X_train, X_test = X[:split_index], X[split_index:]
y_train, y_test = y[:split_index], y[split_index:]


model = XGBRegressor(n_estimators=1000, learning_rate=0.01, max_depth=3, subsample=0.8, colsample_bytree=0.8)
model.fit(X_train, y_train)


y_pred = model.predict(X_test)


rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)

print(f'RMSE: {rmse:.2f}, MAE: {mae:.2f}')


# Korrigiere die Datumswerte für den Plotting-Bereich
test_date_range = combined_data['Date'][-len(y_test):]

plt.figure(figsize=(14, 7))
plt.plot(test_date_range, y_test, label='Tatsächlicher Preis', color='blue')
plt.plot(test_date_range, y_pred, label='Vorhergesagter Preis', color='red', linestyle='dashed')
plt.title('Tatsächlicher vs. Vorhergesagter Goldpreis (letzte 10 Tage)')
plt.xlabel('Datum')
plt.ylabel('Goldpreis')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# Vorhersage für die Zukunft
last_known_data = X[-1].reshape(1, -1)
future_pred_dates = pd.date_range(start='2025-06-09', periods=5, freq='D')
predictions = []

for date in future_pred_dates:
    pred = model.predict(last_known_data)[0]
    predictions.append(pred)
    last_known_data = np.roll(last_known_data, -1)
    last_known_data[0, -1] = pred

# Vorhersagen in DataFrame speichern
prediction_df = pd.DataFrame({
    'date': future_pred_dates,
    'prediction': predictions
})

# Speichern der Vorhersagen
prediction_df.to_csv('gold_price_predictions.csv', index=False)

# Ausgabe der Vorhersagen
print(prediction_df)