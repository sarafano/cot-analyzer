import pandas as pd
import cot_reports as cot
import json

# Lista de alvos do Sniper
assets = {
    "EUR": "EURO CURRENCY",
    "GBP": "BRITISH POUND",
    "CAD": "CANADIAN DOLLAR",
    "GOLD": "GOLD - COMMODITY"
}

try:
    # Vai buscar os dados de 2026 (Ano atual)
    df = cot.cot_year(2026, cot_report_type='traders_in_financial_futures_fut')
    all_data = {}

    for symbol, name in assets.items():
        mask = df['Market_and_Exchange_Names'].str.contains(name, na=False)
        sub_df = df[mask].tail(10) # Pega nas últimas 10 semanas
        
        c_date = [c for c in sub_df.columns if 'Date' in c][0]
        c_long = [c for c in sub_df.columns if 'Lev' in c and 'Long' in c][0]
        c_short = [c for c in sub_df.columns if 'Lev' in c and 'Short' in c][0]
        
        history = []
        for _, row in sub_df.iterrows():
            history.append({
                "date": str(row[c_date]), 
                "net": int(row[c_long] - row[c_short])
            })
        all_data[symbol] = history

    # GRAVA TUDO NO MESMO FICHEIRO
    with open('euro_data.json', 'w') as f:
        json.dump(all_data, f)
    print("Sucesso Total: EUR, GBP, CAD e GOLD prontos!")
except Exception as e:
    print(f"Erro no Robô: {e}")
