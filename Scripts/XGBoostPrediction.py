import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

combined_data = pd.read_csv('gold_with_features_encoded.csv')


window_size = 10

#Rolling window
def create_rolling_features(data, window_size):
    features = []
    target = []
    for start in range(len(data) - window_size):
        end = start + window_size
        features.append(data.iloc[start:end].drop(columns=['Date']).values.flatten())
        target.append(data.iloc[end]['Goldpreis'])
    return np.array(features), np.array(target)

X, y = create_rolling_features(combined_data, window_size)

X_train, X_test = X[:-10], X[-10:]
y_train, y_test = y[:-10], y[-10:]

model = XGBRegressor(n_estimators=1000, learning_rate=0.01, max_depth=3, subsample=0.8, colsample_bytree=0.8)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
print(f'RMSE: {rmse:.2f}, MAE: {mae:.2f}')

last_known_data = X[-1].reshape(1, -1)
tomorrow_pred = model.predict(last_known_data)[0]
print(f"Vorhersage für den 05.06.2025: {tomorrow_pred:.2f}")


# Plot
plt.figure(figsize=(14, 7))
plt.plot(combined_data['Date'][-10:], y_test, label='Tatschlicher Preis', color='blue')
plt.plot(combined_data['Date'][-10:], y_pred, label='Vorhergesagter Preis', color='red', linestyle='dashed')
plt.title('Tatsächlicher vs. Vorhergesagter Goldpreis (letzte 10 Tage)')
plt.xlabel('Datum')
plt.ylabel('Goldpreis')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

