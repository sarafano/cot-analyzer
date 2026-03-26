import pandas as pd
import cot_reports as cot
import json

def update_cot_data():
    # 1. Busca os dados de 2026 (Traders in Financial Futures)
    df = cot.cot_year(2026, cot_report_type='traders_in_financial_futures_fut')
    
    # 2. Filtra o Euro
    euro = df[df['Market_and_Exchange_Names'].str.contains("EURO CURRENCY", na=False)]
    
    # 3. Formata os dados para o gráfico (Data e Net Position)
    euro_history = []
    for _, row in euro.iterrows():
        # Identificar as colunas (os nomes variam)
        col_data = [c for c in euro.columns if 'Date' in c][0]
        col_longs = [c for c in euro.columns if 'Lev_Money_Positions_Long_All' in c][0]
        col_shorts = [c for c in euro.columns if 'Lev_Money_Positions_Short_All' in c][0]
        
        data = row[col_data]
        net = row[col_longs] - row[col_shorts]
        
        # Guardar como objeto JSON
        euro_history.append({"date": data, "net_position": int(net)})
    
    # 4. Grava o ficheiro que o site vai ler
    with open('euro_cot.json', 'w') as f:
        json.dump(euro_history, f)
    
    print("Dados do Euro atualizados com sucesso!")

if __name__ == "__main__":
    update_cot_data()
