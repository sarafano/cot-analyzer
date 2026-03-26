import pandas as pd
import requests
import zipfile
import io
import json

def get_real_data():
    # URL oficial do histórico de 2026 (Legacy Report)
    url = "https://www.cftc.gov/files/dea/history/deahist2026.zip"
    assets = {
        "EUR": "EURO CURRENCY",
        "GBP": "BRITISH POUND",
        "CAD": "CANADIAN DOLLAR",
        "GOLD": "GOLD"
    }
    
    try:
        # Download e extração do ficheiro ZIP
        r = requests.get(url, timeout=30)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        with z.open("annual.txt") as f:
            df = pd.read_csv(f)
            
        final_dict = {}
        for symbol, name in assets.items():
            # Filtro pelo nome oficial no relatório
            mask = df['Market_and_Exchange_Names'].str.contains(name, case=False, na=False)
            sub_df = df[mask].tail(10) # Pega as últimas 10 semanas
            
            if not sub_df.empty:
                history = []
                for _, row in sub_df.iterrows():
                    # Cálculo do Net Position (Institucionais)
                    long = int(row['Noncommercial_Positions_Long_All'])
                    short = int(row['Noncommercial_Positions_Short_All'])
                    # Data real formatada
                    date_val = str(row['As_of_Date_In_Form_YYMMDD'])
                    history.append({"date": date_val, "net": long - short})
                final_dict[symbol] = history
        return final_dict
    except Exception as e:
        print(f"Erro na ligação CFTC: {e}")
        return {}

# Executa e guarda os dados reais
data = get_real_data()
if data:
    with open('euro_data.json', 'w') as f:
        json.dump(data, f)
    print("Sucesso! O ficheiro foi atualizado com dados reais.")
