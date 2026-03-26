import pandas as pd
import cot_reports as cot
import json

try:
    # 1. Vai buscar os dados
    df = cot.cot_year(2026, cot_report_type='traders_in_financial_futures_fut')
    
    # 2. Filtra o Euro
    euro = df[df['Market_and_Exchange_Names'].str.contains("EURO CURRENCY", na=False)].tail(10)
    
    # 3. Descobre os nomes das colunas automaticamente (O segredo para não dar erro)
    c_date = [c for c in euro.columns if 'Date' in c][0]
    c_long = [c for c in euro.columns if 'Lev' in c and 'Long' in c][0]
    c_short = [c for c in euro.columns if 'Lev' in c and 'Short' in c][0]
    
    history = []
    for _, row in euro.iterrows():
        net = int(row[c_long] - row[c_short])
        history.append({"date": str(row[c_date]), "net": net})
    
    # 4. Grava o JSON
    with open('euro_data.json', 'w') as f:
        json.dump(history, f)
    print("Sucesso: euro_data.json criado!")
    
except Exception as e:
    print(f"Erro no processamento: {e}")
    exit(1)
