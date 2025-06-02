import pandas as pd

combined_data = pd.read_csv('../Data/combined_gold_economic_factors.csv')

# Umbenennen der Spalte von "Goldpreis_am_Tag" in "Goldpreis", falls noch nicht geschehen
if 'Goldpreis_am_Tag' in combined_data.columns:
    combined_data.rename(columns={'Goldpreis_am_Tag': 'Goldpreis'}, inplace=True)

# Überprüfe auf fehlende Daten
missing_data = combined_data.isnull().sum()
print("Anzahl der fehlenden Werte in jeder Spalte:")
print(missing_data)

# Test ob "Date"-Spalte im Datetime-Format
combined_data['Date'] = pd.to_datetime(combined_data['Date'])

# neue Spalte die den Wochentag enthält
combined_data['Wochentag'] = combined_data['Date'].dt.day_name()

print(combined_data.head(20))
print(combined_data.groupby(['Wochentag']).count())

gold=pd.read_csv('../Data/Goldpreis.csv')

gold['Date'] = pd.to_datetime(combined_data['Date'])
gold['Wochentag'] = combined_data['Date'].dt.day_name()
print(gold.groupby(['Wochentag']).count())
#combined_data.to_csv('combined_gold_economic_factors_withweekdays.csv', index=False)