import pandas as pd
import cot_reports as cot
import json

# Baixa os dados
df = cot.cot_year(2026, cot_report_type='traders_in_financial_futures_fut')
euro = df[df['Market_and_Exchange_Names'].str.contains("EURO CURRENCY", na=False)].tail(5)

# Pega as colunas certas sem precisar do nome exato
c_data = [c for c in euro.columns if 'Date' in c][0]
c_long = [c for c in euro.columns if 'Lev' in c and 'Long' in c][0]
c_short = [c for c in euro.columns if 'Lev' in c and 'Short' in c][0]

output = []
for _, row in euro.iterrows():
    output.append({"date": str(row[c_data]), "net": int(row[c_long] - row[c_short])})

with open('euro_data.json', 'w') as f:
    json.dump(output, f)
