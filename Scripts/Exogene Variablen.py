# Goldpreisentwicklung

import pandas as pd
import matplotlib.pyplot as plt

# Vorverarbeitung und filtern
df_goldpreis_alles=pd.read_csv('../Data/combined_gold_economic_factors_withweekdays.csv', index_col=0, parse_dates=True) # einlesen
df_goldpreis_alles.index = pd.to_datetime(df_goldpreis_alles.index) #Datum umwandeln
df_goldpreis_alles = df_goldpreis_alles[df_goldpreis_alles.index > pd.Timestamp('2021-01-01')] # nach 2021 filtern

# Plot mit allen exogenen Vars
ax = plt.subplot(1, 1, 1)
plt.title('Preisentwicklung der exogenen Vars')
plt.plot(df_goldpreis_alles['Goldpreis'])
plt.plot(df_goldpreis_alles['Gold_ETF'])
plt.plot(df_goldpreis_alles['Dollar_Index'])
plt.plot(df_goldpreis_alles['SP500'])
plt.plot(df_goldpreis_alles['Oil_Price'])
plt.ylabel('Goldpreis in Dollar pro Feinunze')
plt.legend(['Goldpreis', 'Gold_ETF', 'Dollar_Index', 'SP500', 'Oil_Price'])
plt.xticks(rotation=45)
plt.show()
plt.clf()

# Plot mit Entwicklung der exogenen Vars, in einzelnen Plots
fig = plt.figure(figsize=(14, 10))
fig.suptitle('Einflussfaktoren auf den Goldpreis', fontsize=16)

ax = plt.subplot(2, 3, 1)
plt.title('Goldpreis')
plt.plot(df_goldpreis_alles['Goldpreis'])
plt.xticks(rotation=45)

ax = plt.subplot(2, 3, 2)
plt.title('Dollar Index')
plt.plot(df_goldpreis_alles['Dollar_Index'])
plt.xticks(rotation=45)

ax = plt.subplot(2, 3, 3)
plt.title('Gold ETF')
plt.plot(df_goldpreis_alles['Gold_ETF'])
plt.xticks(rotation=45)

ax = plt.subplot(2, 3, 4)
plt.title('Ölpreis')
plt.plot(df_goldpreis_alles['Oil_Price'])
plt.xticks(rotation=45)

ax = plt.subplot(2, 3, 5)
plt.title('SP500')
plt.plot(df_goldpreis_alles['SP500'])
plt.xticks(rotation=45)
plt.tight_layout()
# fig.autofmt_xdate()
plt.show()
plt.clf()


from sklearn.preprocessing import MinMaxScaler

# Plot mit exogenen Vars normalisiert

cols = ['Goldpreis', 'Gold_ETF', 'Dollar_Index', 'SP500', 'Oil_Price']
scaler = MinMaxScaler()

scaled_data = pd.DataFrame(
    scaler.fit_transform(df_goldpreis_alles[cols]),
    columns=cols,
    index=df_goldpreis_alles.index
)

fig = plt.figure(figsize=(10, 6))
ax = plt.subplot(1, 1, 1)
plt.title('Preisentwicklung der exogenen Vars')
plt.plot(scaled_data['Goldpreis'])
plt.plot(scaled_data['Gold_ETF'])
plt.plot(scaled_data['Dollar_Index'])
plt.plot(scaled_data['SP500'])
plt.plot(scaled_data['Oil_Price'])
plt.ylabel('Goldpreis in Dollar pro Feinunze')
plt.legend(['Goldpreis', 'Gold_ETF', 'Dollar_Index', 'SP500', 'Oil_Price'])
plt.xticks(rotation=45)
plt.show()
plt.clf()

# Korrelationsmatrix berechnen (Pearson-Korrelation)
corr_matrix = df_goldpreis_alles.drop(columns="Wochentag").corr()

print(corr_matrix)

fig = plt.figure(figsize=(10, 6))
ax = plt.subplot(1, 1, 1)
plt.title('Entwicklung von Goldpreis und SP5ßß')
plt.plot(scaled_data['Goldpreis'])
plt.plot(scaled_data['SP500'])
plt.ylabel('Goldpreis in Dollar pro Feinunze')
plt.legend(['Goldpreis', 'SP500'])
plt.xticks(rotation=45)
plt.show()
plt.clf()