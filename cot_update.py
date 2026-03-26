import pandas as pd
import cot_reports as cot
import json

def get_cot_data():
    # Tenta 2025 porque 2026 pode ainda não ter o relatório completo disponível
    try:
        df = cot.cot_year(2025, cot_report_type='legacy_fut')
    except:
        return {}

    assets = {
        "EUR": "EURO CURRENCY",
        "GBP": "BRITISH POUND",
        "CAD": "CANADIAN DOLLAR",
        "GOLD": "GOLD"
    }
    
    final_dict = {}
    
    for symbol, name in assets.items():
        # Filtro simplificado para não falhar
        mask = df['Market_and_Exchange_Names'].str.contains(name, case=False, na=False)
        sub_df = df[mask].tail(10)
        
        if not sub_df.empty:
            history = []
            for _, row in sub_df.iterrows():
                # Cálculo simples: Compras - Vendas
                net = int(row['Noncommercial_Positions_Long_All'] - row['Noncommercial_Positions_Short_All'])
                date = str(row['As_of_Date_In_Form_YYMMDD'])
                history.append({"date": date, "net": net})
            final_dict[symbol] = history
            
    return final_dict

# Executa e grava
data = get_cot_data()
with open('euro_data.json', 'w') as f:
    json.dump(data, f)

if data:
    print("SUCESSO: Dados encontrados!")
else:
    print("ERRO: O ficheiro continuou vazio.")
