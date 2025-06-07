import requests
import pandas as pd

# Replace with your actual FRED API key
API_KEY = "511825a88517acb32e2e595890e51945"

# URL and parameters for FRED API
url = "https://api.stlouisfed.org/fred/series/observations"
params = {
    "series_id": "FEDFUNDS",  # Federal Funds Effective Rate
    "api_key": API_KEY,
    "file_type": "json",
    "observation_start": "2021-01-01"
}

# Get the data
response = requests.get(url, params=params)
data = response.json()["observations"]

# Convert to DataFrame
df = pd.DataFrame(data)

# Clean the data
df = df[["date", "value"]]
df["date"] = pd.to_datetime(df["date"])
df["value"] = pd.to_numeric(df["value"], errors="coerce")

# Drop missing values (if any)
df.dropna(inplace=True)

# Save to CSV
df.to_csv("interest_rate_2021_2025.csv", index=False)

print("CSV file saved: interest_rate_2021_2025.csv")
