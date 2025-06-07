import pandas as pd

# Bundesbank interest rate CSV URL
# SU0102 = 3-month EURIBOR (Germany, daily where available)
url = "https://www.bundesbank.de/statistic-rmi/StatisticDownload?tsId=BBK01.SU0102&its_csvFormat=en&mode=its"


# Read the CSV file (skip first metadata rows)
df = pd.read_csv(url, skiprows=5)

# Rename columns
df.columns = ["Date", "Interest Rate"]

# Convert date strings to datetime objects
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

# Drop rows with missing dates or values
df.dropna(inplace=True)

# Filter for dates from 2001 onwards
df = df[df["Date"] >= "2021-01-01"]

# Save to CSV
df.to_csv("germany_interest_rate_2001_2025.csv", index=False)

print("Saved as germany_interest_rate_2001_2025.csv")








# import pandas as pd
#
# # Load data from Bundesbank (e.g., 3-month interest rate)
# url = "https://www.bundesbank.de/statistic-rmi/StatisticDownload?tsId=BBK01.SU0102&its_csvFormat=en&mode=its"
# df = pd.read_csv(url, skiprows=5)
#
# # Clean and format
# df.columns = ["Date", "Interest Rate"]
# df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
# df.dropna(inplace=True)
#
# # Save to CSV
# df.to_csv("germany_interest_rate.csv", index=False)
# print("Germany interest rate data saved.")
