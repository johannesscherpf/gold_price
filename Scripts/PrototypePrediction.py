import pandas as pd

gold_data = pd.read_csv('Goldpreis.csv', index_col=0)
gold_data.reset_index(inplace=True)
gold_data.columns = ['Date', 'Goldpreis_am_Tag']

if 'Goldpreis_am_Tag' in gold_data.columns:
    gold_data.rename(columns={'Goldpreis_am_Tag': 'Goldpreis'}, inplace=True)

#Auf Null Werte prüfen
missing_data = gold_data.isnull().sum()
print("Anzahl der fehlenden Werte in jeder Spalte:")
print(missing_data)


gold_data['Date'] = pd.to_datetime(gold_data['Date'])

# Wochentage/Monat/Quartal aus Datum extrahieren
gold_data['Wochentag'] = gold_data['Date'].dt.day_name()
gold_data['Monat'] = gold_data['Date'].dt.month_name()
gold_data['Quartal'] = gold_data['Date'].dt.quarter
gold_data['Tag'] = gold_data['Date'].dt.day
gold_data['Jahr'] = gold_data['Date'].dt.year


# One-Hot-Encoding für Wochentage
weekday_dummies = pd.get_dummies(gold_data['Wochentag'], prefix='Weekday')
gold_data = pd.concat([gold_data, weekday_dummies], axis=1)

day_dummies = pd.get_dummies(gold_data['Tag'], prefix='Tag')
gold_data = pd.concat([gold_data, day_dummies], axis=1)

monat_dummies = pd.get_dummies(gold_data['Monat'], prefix='Monat')
gold_data = pd.concat([gold_data, monat_dummies], axis=1)

quartalsdummies = pd.get_dummies(gold_data['Quartal'], prefix='Quartal')
gold_data = pd.concat([gold_data, monat_dummies, quartalsdummies], axis=1)

jahr_dummies = pd.get_dummies(gold_data['Jahr'], prefix='Jahr')
gold_data = pd.concat([gold_data, jahr_dummies], axis=1)


gold_data.sort_values(by='Date', ascending=False, inplace=True)
gold_data['Preisänderung'] = gold_data['Goldpreis'].pct_change(periods=-1) * 100


gold_data = gold_data[gold_data['Date'] >= '2021-01-01']
gold_data.sort_values(by='Date', inplace=True, ascending=False)
print(gold_data.head(20))


gold_data.sort_values(by='Date', ascending=True, inplace=True)

encoded_gold_data=gold_data.drop(columns=['Wochentag','Monat','Quartal'])

encoded_gold_data.to_csv('gold_with_features_encoded.csv', index=False)