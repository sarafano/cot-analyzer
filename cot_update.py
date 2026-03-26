import pandas as pd
import cot_reports as cot
import json

# Nomes simplificados para máxima compatibilidade
assets_map = {
    "EUR": "EURO CURRENCY",
    "GBP": "BRITISH POUND",
    "CAD": "CANADIAN DOLLAR",
    "GOLD": "GOLD"
}

def get_data():
    all_results = {}
    # Tenta 2026, se falhar ou estiver vazio, tenta 2025
    for year in [2026, 2025]:
        try:
            print(f"A tentar obter dados de {year}...")
            df = cot.cot_year(year, cot_report_type='legacy_fut')
            
            if df is None or df.empty:
                continue

            for symbol, search_term in assets_map.items():
                # Filtra pelo nome do ativo
                mask = df['Market_and_Exchange_Names'].str.contains(search_term, case=False, na=False)
                sub_df = df[mask].tail(12)
                
                if not sub_df.empty:
                    history = []
                    for _, row in sub_df.iterrows():
                        # Cálculo da Posição Líquida (Longs - Shorts)
                        net = int(row['Noncommercial_Positions_Long_All'] - row['Noncommercial_Positions_Short_All'])
                        # Formata a data (YYMMDD)
                        date_str = str(row['As_of_Date_In_Form_YYMMDD'])
                        history.append({"date": date_str, "net": net})
                    
                    all_results[symbol] = history
                    print(f"✅ {symbol} extraído com sucesso ({year}).")
            
            # Se já encontrou dados (pelo menos do EUR), não precisa de tentar outro ano
            if all_results:
                break
        except Exception as e:
            print(f"Erro ao processar ano {year}: {e}")
            continue
            
    return all_results

# Execução principal
try:
    data_to_save = get_data()
    
    if not data_to_save:
        print("ERRO CRÍTICO: Nenhum dado foi encontrado!")
        # Cria um dado de teste para o site não ficar em branco se tudo falhar
        data_to_save = {"EUR": [{"date": "260326", "net": 0}]}

    with open('euro_data.json', 'w') as f:
        json.dump(data_to_save, f)
    print("Ficheiro euro_data.json atualizado!")

except Exception as e:
    print(f"Falha fatal: {e}")
