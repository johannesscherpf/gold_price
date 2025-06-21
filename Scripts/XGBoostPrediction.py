import csv

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import TimeSeriesSplit

# Daten laden und vorbereiten
combined_data = pd.read_csv('../data/combined_gold_economic_factors_withweekdays.csv')
combined_data['Date'] = pd.to_datetime(combined_data['Date'])
combined_data.sort_values(by='Date', ascending=True, inplace=True)

#Spalten auswählen die benutzt werden sollen
combined_data = combined_data[['Date','Goldpreis','Goldpreis_gestern','SP500','Oil_Price','Gold_ETF']]
#Zeitraum der Daten auswählen
combined_data = combined_data[combined_data['Date'] >= '2021-01-01']

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

#Tesstdaten/Trainingsdaten ausgeben
'''
Y_trainprint= pd.DataFrame(y_train)
Y_trainprint.to_csv('Ytrain.csv', index=True)
X_trainprint= pd.DataFrame(X_train)
X_trainprint.to_csv('Xtrain.csv', index=True)
Y_testprint= pd.DataFrame(y_test)
Y_testprint.to_csv('Ytest.csv', index=True)
X_testprint= pd.DataFrame(X_test)
X_testprint.to_csv('Xtest.csv', index=True)
'''

# Hyperparameter-Tuning
param_grid = {
    'n_estimators': [ 500,750, 1000],
    'learning_rate': [0.001,0.005,0.01, 0.1],
    'max_depth': [3, 5],
    'subsample': [ 0.8, 1.0],
    'colsample_bytree': [0,0.2,0.8, 1.0]
}
#random split in xgboost ersetzen durch timeseries split
tscv = TimeSeriesSplit(n_splits=5)

xgb = XGBRegressor(objective='reg:squarederror')
grid_search = GridSearchCV(estimator=xgb, param_grid=param_grid ,scoring='neg_mean_absolute_error', cv=tscv, verbose=3, n_jobs=-1)
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

first_date = combined_data['Date'].min()
last_date = combined_data['Date'].max()
columns = combined_data.columns.tolist()

results_csv = '../data/XGBoostDaten/grid_search_results.csv'
with open(results_csv, mode='a', newline='') as file:
    writer = csv.writer(file)
    # Header schreiben, falls die Datei neu ist
    writer.writerow(['first_date', 'last_date', 'columns', 'best_params', 'mean_test_score','rmse','mae'])
    # Ergebnis schreiben
    writer.writerow([first_date, last_date, columns, grid_search.best_params_, grid_search.best_score_,rmse,mae])

# Visualisierung der Vorhersagen
test_date_range = combined_data['Date'][-len(y_test):]

plt.figure(figsize=(14, 7))
plt.plot(test_date_range, y_test, label='Tatsächlicher Preis', color='blue')
plt.plot(test_date_range, y_pred, label='Vorhergesagter Preis', color='lightblue', linestyle='dashed')


#Beste Parameter: {'colsample_bytree': 0.8, 'learning_rate': 0.1, 'max_depth': 3, 'n_estimators': 1000, 'subsample': 0.8}

# Vorhersage für die Zukunft vorbereiten
last_known_data = X[-1].reshape(1, -1)
future_pred_dates = pd.date_range(start='2025-06-09', periods=5, freq='B')
predictions = []

#Vorhersage des Goldpreises
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




cv_results = pd.DataFrame(grid_search.cv_results_)
pivot_table = cv_results.pivot_table(values='mean_test_score',
                                     index='param_n_estimators',
                                     columns='param_max_depth')

plt.figure(figsize=(10, 7))
sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap="YlGnBu")
plt.title('Hyperparameter-Tuning: Negative MSE von n_estimators vs max_depth')
plt.xlabel('Max Depth')
plt.ylabel('N Estimators')
plt.show()

prediction_df = pd.DataFrame({
    'date': future_pred_dates,
    'prediction': predictions
})


prediction_df.to_csv('../data/XGBoostDaten/gold_price_predictions.csv', index=False)
print(prediction_df)