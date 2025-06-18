import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import GridSearchCV

# Daten laden und vorbereiten
combined_data = pd.read_csv('../data/combined_gold_economic_factors_withweekdays.csv')
combined_data['Date'] = pd.to_datetime(combined_data['Date'])
#combined_data.sort_values(by='Date', ascending=True, inplace=True)
combined_data = combined_data[['Date', 'Goldpreis']]


window_size = 20
lag_size = 10
def create_rolling_features(data, window_size, lag_size):
    features = []
    target = []
    for start in range(len(data) - window_size - lag_size):
        end = start + window_size
        features.append(data.iloc[start:end]['Goldpreis'].values.flatten())
        target.append(data.iloc[end + lag_size]['Goldpreis'])
    return np.array(features), np.array(target)

X, y = create_rolling_features(combined_data, window_size, lag_size)

# Train-Test-Split
split_index = len(X) - 10
X_train, X_test = X[:split_index], X[split_index:]
y_train, y_test = y[:split_index], y[split_index:]

# Hyperparameter-Tuning
param_grid = {
    'n_estimators': [100, 500, 1000],
    'learning_rate': [0.01, 0.1],
    'max_depth': [3, 5],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

xgb = XGBRegressor(objective='reg:squarederror')
grid_search = GridSearchCV(estimator=xgb, param_grid=param_grid, scoring='neg_mean_squared_error', cv=3, verbose=2, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Beste Parameter und Modell
print(f"Beste Parameter: {grid_search.best_params_}")
best_model = grid_search.best_estimator_

# Vorhersagen
y_pred = best_model.predict(X_test)

# Fehlermaße
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
print(f'RMSE: {rmse:.2f}, MAE: {mae:.2f}')

# Visualisierung der Vorhersagen
test_date_range = combined_data['Date'][-len(y_test):]

plt.figure(figsize=(14, 7))
plt.plot(test_date_range, y_test, label='Tatsächlicher Preis', color='blue')
plt.plot(test_date_range, y_pred, label='Vorhergesagter Preis', color='lightblue', linestyle='dashed')




# Vorhersage für die Zukunft
last_known_data = X[-1].reshape(1, -1)
future_pred_dates = pd.date_range(start='2025-06-18', periods=10, freq='B')
predictions = []

for date in future_pred_dates:
    pred = best_model.predict(last_known_data)[0]
    predictions.append(pred)
    last_known_data = np.roll(last_known_data, -1)
    last_known_data[0, -1] = pred

#Vorhersagen plotten
plt.plot(future_pred_dates, predictions, label='Zukünftige Vorhersagen', color='red', linestyle='--', marker='o')

plt.title('Tatsächlicher vs. Vorhergesagter Goldpreis')
plt.xlabel('Datum')
plt.ylabel('Goldpreis')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()


#Beste Parameter: {'colsample_bytree': 0.8, 'learning_rate': 0.1, 'max_depth': 3, 'n_estimators': 1000, 'subsample': 0.8}



prediction_df = pd.DataFrame({
    'date': future_pred_dates,
    'prediction': predictions
})


prediction_df.to_csv('gold_price_predictions.csv', index=False)
print(prediction_df)