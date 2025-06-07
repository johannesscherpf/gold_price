import pandas as pd

#Load your dataset
df = pd.read_csv("UNRATE.csv")

#Convert 'UNRATE' to numeric, forcing invalid values (like text) to NaN
df["UNRATE"] = pd.to_numeric(df["UNRATE"], errors="coerce")

## Optional: Entfernen Sie unrealistische Werte (z. B. negativ oder > 100 %)

df = df[(df["UNRATE"] >= 0)&(df["UNRATE"] <= 100)]

# Bereinigten Datensatz speichern

df.to_csv("cleaned unemployment.csv", index=False)
print("Cleaned data saved as cleaned_unemployment.csv")







# import pandas as pd

# df = pd.read_csv('UNRATE.csv')



# print(df.to_string())