import yfinance as yf
import pandas as pd

# Zeitspanne für die Datenabrufung (Format : "YYYY-MM-DD")
start_date = "2021-01-01"
end_date = "2025-05-15"

# Symbol für Gold (nicht echter Goldpreis nur ein Gold ETF als Proxy)
gold_ticker = 'GLD'
gold_data = yf.download(gold_ticker, start=start_date, end=end_date, interval='1d')[['Close']]

# US-Dollar-Index
dxy_ticker = 'DX-Y.NYB'
dxy_data = yf.download(dxy_ticker, start=start_date, end=end_date, interval='1d')[['Close']]

# S&P 500 Index
sp500_ticker = '^GSPC'
sp500_data = yf.download(sp500_ticker, start=start_date, end=end_date, interval='1d')[['Close']]

# Rohölpreise
oil_ticker = 'CL=F'
oil_data = yf.download(oil_ticker, start=start_date, end=end_date, interval='1d')[['Close']]

# Kombiniere alle DataFrames
combined_data = pd.concat([
    gold_data.rename(columns={'Close': 'Gold_ETF'}),
    dxy_data.rename(columns={'Close': 'Dollar_Index'}),
    sp500_data.rename(columns={'Close': 'SP500'}),
    oil_data.rename(columns={'Close': 'Oil_Price'})
], axis=1).dropna()

# Index als Spalte umwandeln
combined_data.reset_index(inplace=True)

combined_data.to_csv('../Data/economic_factors.csv', index=False)

