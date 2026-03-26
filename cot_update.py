import pandas as pd
import cot_reports as cot
import json

# Nomes simplificados para o filtro ser mais eficaz
assets_map = {
    "EUR": "EURO CURRENCY",
    "GBP": "BRITISH POUND",
    "CAD": "CANADIAN DOLLAR",
    "GOLD": "GOLD"
}

def get_data():
    all_results = {}
    # Tenta primeiro 2026, se falhar tenta 2025
    for year in [2026, 2025]:
        try:
            print(f"A tentar ano {year}...")
            df = cot.cot_year(year, cot_report_type='legacy_fut')
            if df.empty: continue

            for symbol, search_term in assets_map.items():
                if symbol in all_results: continue # Já encontrou dados
                
                mask = df['Market_and_Exchange_Names'].str.contains(search_term, case=False, na=False)
                sub_df = df[mask].tail(15)
                
                if not sub_df.empty:
                    history = []
                    for _, row in sub_df.iterrows():
                        # Cálculo: Compras - Vendas (Non-Commercial / Institucionais)
                        net = int(row['Noncommercial_Positions_Long_All'] - row['Noncommercial_Positions_Short_All'])
                        date_str = str(row['As_of_Date_In_Form_YYMMDD'])
                        history.append({"date": date_str, "net": net})
                    all_results[symbol] = history
                    print(f"✅ {symbol} encontrado em {year}")
            
            if len(all_results) == len(assets_map): break # Já tem tudo
        except:
            continue
    return all_results

try:
    final_data = get_data()
    with open('euro_data.json', 'w') as f:
        json.dump(final_data, f)
    print("Processo concluído!")
except Exception as e:
    print(f"Erro: {e}")
