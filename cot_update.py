import pandas as pd
import cot_reports as cot
import json

# Busca dados de 2026
df = cot.cot_year(2026, cot_report_type='traders_in_financial_futures_fut')
euro = df[df['Market_and_Exchange_Names'].str.contains("EURO CURRENCY", na=False)].tail(5)

# Pega os nomes das colunas que existem de verdade
cols = euro.columns
d_col = [c for c in cols if 'Date' in c][0]
l_col = [c for c in cols if 'Lev_Money_Positions_Long_All' in c][0]
s_col = [c for c in cols if 'Lev_Money_Positions_Short_All' in c][0]

dados_finais = []
for _, row in euro.iterrows():
    dados_finais.append({
        "data": str(row[d_col]),
        "net": int(row[l_col] - row[s_col])
    })

with open('euro_data.json', 'w') as f:
    json.dump(dados_finais, f)
