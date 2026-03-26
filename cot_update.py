import pandas as pd
import cot_reports as cot
import json

assets = {
    "EUR": "EURO CURRENCY",
    "GBP": "BRITISH POUND",
    "CAD": "CANADIAN DOLLAR",
    "GOLD": "GOLD - COMMODITY"
}

try:
    df = cot.cot_year(2026, cot_report_type='traders_in_financial_futures_fut')
    all_data = {}

    for symbol, name in assets.items():
        # Filtra o ativo
        mask = df['Market_and_Exchange_Names'].str.contains(name, na=False)
        sub_df = df[mask].tail(10)
        
        # Identifica colunas (evita o KeyError anterior)
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

    with open('euro_data.json', 'w') as f:
        json.dump(all_data, f)
    print("Sucesso: EUR, GBP, CAD e GOLD atualizados!")
except Exception as e:
    print(f"Erro: {e}")
