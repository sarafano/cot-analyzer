import pandas as pd
import cot_reports as cot
import json

# Nomes exatos para o relatório LEGACY
assets = {
    "EUR": "EURO CURRENCY - CHICAGO MERCANTILE EXCHANGE",
    "GBP": "BRITISH POUND STERLING - CHICAGO MERCANTILE EXCHANGE",
    "CAD": "CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE",
    "GOLD": "GOLD - COMMODITY EXCHANGE INC."
}

try:
    # Mudança para 'legacy_fut' (o mais robusto)
    df = cot.cot_year(2026, cot_report_type='legacy_fut')
    all_data = {}

    for symbol, name in assets.items():
        mask = df['Market_and_Exchange_Names'].str.contains(name, case=False, na=False)
        sub_df = df[mask].tail(12)
        
        if not sub_df.empty:
            # No Legacy, os institucionais são 'Noncommercial'
            c_date = [c for c in sub_df.columns if 'As_of_Date' in c][0]
            c_long = 'Noncommercial_Positions_Long_All'
            c_short = 'Noncommercial_Positions_Short_All'
            
            history = []
            for _, row in sub_df.iterrows():
                history.append({
                    "date": str(row[c_date]).split(' ')[0], 
                    "net": int(row[c_long] - row[row[c_short]])
                })
            all_data[symbol] = history

    with open('euro_data.json', 'w') as f:
        json.dump(all_data, f)
    print("Dados Legacy gravados!")
except Exception as e:
    # Se falhar, tenta 2025 só para popular o gráfico
    df = cot.cot_year(2025, cot_report_type='legacy_fut')
    # ... mesma lógica ...
    print(f"Erro: {e}")
