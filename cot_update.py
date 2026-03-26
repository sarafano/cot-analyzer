import pandas as pd
import cot_reports as cot
import json
import os

def get_data():
    # 1. Baixa dados de 2026
    df = cot.cot_year(2026, cot_report_type='traders_in_financial_futures_fut')
    
    # 2. Filtra o Euro e pega as últimas 10 semanas para o gráfico
    euro = df[df['Market_and_Exchange_Names'].str.contains("EURO CURRENCY", na=False)].tail(10)
    
    history = []
    for _, row in euro.iterrows():
        # Identifica colunas dinamicamente para evitar erros
        c_date = [c for c in euro.columns if 'Date' in c][0]
        c_long = [c for c in euro.columns if 'Lev_Money_Positions_Long_All' in c][0]
        c_short = [c for c in euro.columns if 'Lev_Money_Positions_Short_All' in c][0]
        
        net = int(row[c_long] - row[c_short])
        history.append({"date": str(row[c_date]), "net": net})

    # 3. Guarda o JSON que o teu index.html vai usar
    with open('euro_data.json', 'w') as f:
        json.dump(history, f)

if __name__ == "__main__":
    get_data()
