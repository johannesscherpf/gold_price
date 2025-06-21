import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

# Daten laden und vorbereiten
gold_df = pd.read_csv('../data/Goldpreis.csv')
gold_df['Date'] = pd.to_datetime(gold_df['Date'])
gold_df.set_index('Date', drop=True, inplace=True)

# Vorheriger Goldpreis generieren
gold_df['Goldpreis_gestern'] = gold_df['Goldpreis'].shift(1)
gold_df = gold_df.dropna()
gold_df.columns = ['Goldpreis', 'Goldpreis_gestern']
gold_df['Goldpreis'] = gold_df['Goldpreis'].astype(float)

# Skalieren der Daten
scaler = MinMaxScaler()
gold_df = pd.DataFrame(data=scaler.fit_transform(gold_df), columns=gold_df.columns, index=gold_df.index)

# Zeitweilige Einordnung nach 2020 als Split
base_date = '2020-01-01'
train = gold_df.loc[gold_df.index < base_date]
valid = gold_df.loc[gold_df.index >= base_date]

# Konvertieren zu Arrays ohne festes reshape
X_train = np.array(train['Goldpreis']).reshape(-1, 1)
y_train = np.array(train['Goldpreis_gestern']).reshape(-1, 1)
X_valid = np.array(valid['Goldpreis']).reshape(-1, 1)
y_valid = np.array(valid['Goldpreis_gestern']).reshape(-1, 1)

print(f"Trainingsdatenformate: {X_train.shape}, {y_train.shape}")
print(f"Validierungsdatenformate: {X_valid.shape}, {y_valid.shape}")

# Hyperparameter-Tuning mit RandomizedSearchCV und GridSearchCV
xgb_params = {
    'booster': ['gblinear'],
    'objective': ['reg:squarederror', 'reg:squaredlogerror'],
    'eval_metric': ['mae', 'rmse']
}

xgb_randomized_search = RandomizedSearchCV(XGBRegressor(), param_distributions=xgb_params, n_iter=4, cv=3)
xgb_randomized_search_results = xgb_randomized_search.fit(X_train, y_train)

xgb_grid_search = GridSearchCV(XGBRegressor(), param_grid=xgb_params, cv=3)
xgb_grid_search_results = xgb_grid_search.fit(X_train, y_train)

print(f"Beste Parameter aus RandomizedSearch: {xgb_randomized_search_results.best_params_}")
print(f"Beste Parameter aus GridSearch: {xgb_grid_search_results.best_params_}")

# Finale Modellanpassung mit besten Parametern
xgb_reg = XGBRegressor(
    booster=xgb_grid_search_results.best_params_['booster'],
    eval_metric=xgb_grid_search_results.best_params_['eval_metric'],
    objective=xgb_grid_search_results.best_params_['objective']
)
xgb_reg.fit(X_train, y_train)

