import pandas as pd
import requests
import zipfile
import io
import json

def get_real_data():
    # URL oficial dos dados de 2026
    url = "https://www.cftc.gov/files/dea/history/deahist2026.zip"
    assets = {
        "EUR": "EURO CURRENCY",
        "GBP": "BRITISH POUND",
        "CAD": "CANADIAN DOLLAR",
        "GOLD": "GOLD"
    }
    
    try:
        # Faz o download do ZIP e extrai os dados
        r = requests.get(url, timeout=30)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        with z.open("annual.txt") as f:
            df = pd.read_csv(f)
            
        final_dict = {}
        for symbol, name in assets.items():
            # Filtra pelo nome do ativo e pega as últimas 10 semanas
            sub_df = df[df['Market_and_Exchange_Names'].str.contains(name, case=False, na=False)].tail(10)
            
            if not sub_df.empty:
                history = []
                for _, row in sub_df.iterrows():
                    long = int(row['Noncommercial_Positions_Long_All'])
                    short = int(row['Noncommercial_Positions_Short_All'])
                    # Extrai a data real do relatório
                    date = str(row['As_of_Date_In_Form_YYMMDD'])
                    history.append({"date": date, "net": long - short})
                final_dict[symbol] = history
        return final_dict
    except Exception as e:
        print(f"Erro ao aceder aos dados reais: {e}")
        return {}

# Executa e guarda no ficheiro
data = get_real_data()
if data:
    with open('euro_data.json', 'w') as f:
        json.dump(data, f)
    print("Sucesso! Dados de Março 2026 carregados.")
