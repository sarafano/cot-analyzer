import pandas as pd
import cot_reports as cot
import json

def get_data():
    assets = {"EUR": "EURO CURRENCY", "GBP": "BRITISH POUND", "CAD": "CANADIAN DOLLAR", "GOLD": "GOLD"}
    all_results = {}
    
    try:
        # Em vez de ano, pedimos os dados mais recentes de moedas e ouro
        df_curr = cot.logger_report(report_type='legacy_fut') 
        
        for symbol, name in assets.items():
            mask = df_curr['Market_and_Exchange_Names'].str.contains(name, case=False, na=False)
            sub_df = df_curr[mask].tail(12)
            
            if not sub_df.empty:
                history = []
                for _, row in sub_df.iterrows():
                    long = int(row['Noncommercial_Positions_Long_All'])
                    short = int(row['Noncommercial_Positions_Short_All'])
                    date = str(row['As_of_Date_In_Form_YYMMDD'])
                    history.append({"date": date, "net": long - short})
                all_results[symbol] = history
    except Exception as e:
        print(f"Erro: {e}")
        
    return all_results

data = get_data()
with open('euro_data.json', 'w') as f:
    json.dump(data, f)
