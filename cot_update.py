import pandas as pd
import cot_reports as cot
import json
import time

assets = {
    "EUR": "EURO CURRENCY",
    "GBP": "BRITISH POUND",
    "CAD": "CANADIAN DOLLAR",
    "GOLD": "GOLD"
}

def fetch_with_retry(year):
    print(f"A tentar obter dados de {year}...")
    try:
        # Tentamos o relatório Legacy que é o mais estável
        df = cot.cot_year(year, cot_report_type='legacy_fut')
        if df is not None and not df.empty:
            return df
    except:
        print(f"Falha ao aceder a {year}")
    return None

# Tenta 2026, se falhar tenta 2025
df = fetch_with_retry(2026)
if df is None or df.empty:
    df = fetch_with_retry(2025)

all_data = {}

if df is not None and not df.empty:
    for symbol, name in assets.items():
        mask = df['Market_and_Exchange_Names'].str.contains(name, case=False, na=False)
        sub_df = df[mask].tail(15)
        
        if not sub_df.empty:
            history = []
            for _, row in sub_df.iterrows():
                try:
                    # Garantir que os dados são convertidos para tipos nativos do Python (int/str)
                    long = int(row['Noncommercial_Positions_Long_All'])
                    short = int(row['Noncommercial_Positions_Short_All'])
                    date = str(row['As_of_Date_In_Form_YYMMDD'])
                    history.append({"date": date, "net": long - short})
                except:
                    continue
            if history:
                all_data[symbol] = history

# Se mesmo assim estiver vazio, cria um dado de teste para não quebrar o site
if not all_data:
    all_data = {"EUR": [{"date": "ERRO", "net": 0}]}

with open('euro_data.json', 'w') as f:
    json.dump(all_data, f)

print("Operação finalizada com dados de:", "2026" if df is not None and '2026' in str(df.iloc[0]) else "2025")
