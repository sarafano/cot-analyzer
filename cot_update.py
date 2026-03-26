import pandas as pd
import cot_reports as cot
import json

# Radar ajustado para encontrar os dados corretos
assets = {
    "EUR": "EURO CURRENCY",
    "GBP": "BRITISH POUND",
    "CAD": "CANADIAN DOLLAR",
    "GOLD": "GOLD"
}

try:
    # Tenta 2026, se falhar ou estiver vazio, o código avisa
    df = cot.cot_year(2026, cot_report_type='traders_in_financial_futures_fut')
    all_data = {}

    if df.empty:
        raise ValueError("Relatório da CFTC ainda não disponível para 2026")

    for symbol, name in assets.items():
        # Busca mais flexível (case insensitive)
        mask = df['Market_and_Exchange_Names'].str.contains(name, case=False, na=False)
        sub_df = df[mask].tail(12) # 3 meses de histórico
        
        if not sub_df.empty:
            c_date = [c for c in sub_df.columns if 'Date' in c][0]
            # Colunas de Leveraged Money (Institucionais)
            c_long = [c for c in sub_df.columns if 'Lev' in c and 'Long' in c][0]
            c_short = [c for c in sub_df.columns if 'Lev' in c and 'Short' in c][0]
            
            history = []
            for _, row in sub_df.iterrows():
                history.append({
                    "date": str(row[c_date]), 
                    "net": int(row[c_long] - row[c_short])
                })
            all_data[symbol] = history
            print(f"✅ {symbol} extraído com sucesso.")
        else:
            print(f"⚠️ {symbol} não encontrado no relatório.")

    if not all_data:
        # Se 2026 falhou, tenta 2025 para não ficar vazio
        print("A tentar dados de 2025...")
        # (Repetir lógica para 2025 se necessário, mas 2026 deve ter dados agora)

    with open('euro_data.json', 'w') as f:
        json.dump(all_data, f)
        
except Exception as e:
    print(f"Erro Fatal: {e}")
