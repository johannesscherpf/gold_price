import pandas as pd

# Lade die bestehende CSV mit Goldpreisen, wobei das Datum als Index verwendet wird
gold_price_csv_file = 'Goldpreis.csv'
# Beim Einlesen den Index zurück in eine Spalte konvertieren
gold_data_existing = pd.read_csv(gold_price_csv_file, index_col=0)
gold_data_existing.reset_index(inplace=True)
gold_data_existing.columns = ['Date', 'Goldpreis_am_Tag']  # Ich nehme an, die einzige Spalte heißt eigtl. "Gold_Price"

# Lade die neue CSV-Datei mit den wirtschaftlichen Faktoren
economic_factors_csv_file = 'economic_factors.csv'
economic_data = pd.read_csv(economic_factors_csv_file)

# Stelle sicher, dass die "Date"-Spalten im richtigen Datumsformat sind
gold_data_existing['Date'] = pd.to_datetime(gold_data_existing['Date'])
economic_data['Date'] = pd.to_datetime(economic_data['Date'])

# Setze das Startdatum und ermittle das letzte gemeinsame Datum
start_union_date = pd.to_datetime('2021-01-01')
latest_common_date = min(gold_data_existing['Date'].max(), economic_data['Date'].max())

# Filtere beide DataFrames auf den Bereich zwischen dem Startdatum und dem letzten gemeinsamen Datum
filtered_gold_data = gold_data_existing[(gold_data_existing['Date'] >= start_union_date) &
                                        (gold_data_existing['Date'] <= latest_common_date)]
filtered_economic_data = economic_data[(economic_data['Date'] >= start_union_date) &
                                       (economic_data['Date'] <= latest_common_date)]

# Vereine beide DataFrames basierend auf dem Datum
combined_data = pd.merge(filtered_gold_data, filtered_economic_data, on='Date', how='inner')

# Speichere das kombinierte Dataset in einer neuen CSV-Datei
combined_csv_filename = 'combined_gold_economic_factors.csv'
combined_data.to_csv(combined_csv_filename, index=False)

print(f"Vereinigte Daten erfolgreich in {combined_csv_filename} gespeichert.")