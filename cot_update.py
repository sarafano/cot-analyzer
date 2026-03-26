import pandas as pd
import requests
import zipfile
import io
import json

def get_cot_data():
    # URL direto do ficheiro zip da CFTC para 2026 (Legacy Report)
    url = "https://www.cftc.gov/files/dea/history/deahist2026.zip"
    assets = {
        "EUR": "EURO CURRENCY",
        "GBP": "BRITISH POUND",
        "CAD": "CANADIAN DOLLAR",
        "GOLD": "GOLD"
    }
    
    try:
        r = requests.get(url, timeout=30)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        # O ficheiro dentro do zip chama-se annual.txt
        with z.open("annual.txt") as f:
            df = pd.read_csv(f)
            
        final_dict = {}
        for symbol, name in assets.items():
            # Filtro por nome do mercado
            sub_df = df[df['Market_and_Exchange_Names'].str.contains(name, case=False, na=False)].tail(12)
            
            if not sub_df.empty:
                history = []
                for _, row in sub_df.iterrows():
                    long = int(row['Noncommercial_Positions_Long_All'])
                    short = int(row['Noncommercial_Positions_Short_All'])
                    # Formato de data: YYMMDD
                    date = str(row['As_of_Date_In_Form_YYMMDD'])
                    history.append({"date": date, "net": long - short})
                final_dict[symbol] = history
        return final_dict
    except Exception as e:
        print(f"Erro ao baixar dados de 2026: {e}")
        return {}

# Executa e guarda
data = get_cot_data()
if data:
    with open('euro_data.json', 'w') as f:
        json.dump(data, f)
    print("✅ Robô automatizado com sucesso!")
else:
    print("❌ Falha na recolha automática.")
