import pandas as pd
import cot_reports as cot
import json

try:
    df = cot.cot_year(2026, cot_report_type='traders_in_financial_futures_fut')
    euro = df[df['Market_and_Exchange_Names'].str.contains("EURO CURRENCY", na=False)].tail(10)
    
    # Esta parte evita o erro do teu print do Colab:
    col_date = [c for c in euro.columns if 'Date' in c][0]
    col_long = [c for c in euro.columns if 'Lev_Money_Positions_Long_All' in c][0]
    col_short = [c for c in euro.columns if 'Lev_Money_Positions_Short_All' in c][0]
    
    history = []
    for _, row in euro.iterrows():
        history.append({
            "date": str(row[col_date]), 
            "net": int(row[col_long] - row[col_short])
        })

    with open('euro_data.json', 'w') as f:
        json.dump(history, f)
    print("Dados gravados!")
except Exception as e:
    print(f"Erro detetado: {e}")
