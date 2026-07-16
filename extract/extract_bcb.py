from datetime import datetime, timedelta
import pandas as pd
import requests
from db import get_engine
from sqlalchemy import text

engine = get_engine()


today = datetime.now()
ten_yeras_ago = today - timedelta(days=3652)
init_date = ten_yeras_ago.strftime("%d/%m/%Y")
final_date = today.strftime("%d/%m/%Y")

series = {
    "selic":432,
    "ipca": 433,
    "dolar": 1,
    "cdi": 12
}

def extrair_serie(cod, name):

    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{cod}/dados?formato=json&dataInicial={init_date}&dataFinal={final_date}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    res = requests.get(url, headers=headers)
    # print(f"Status Code: {res.status_code}")

    if res.status_code == 200:
        data = res.json()
        
        # Criar o DataFrame
        df = pd.DataFrame(data)

        df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
        df['valor'] = df['valor'].astype(float)
        df['indicador'] = name

        return df

    else:
        print("\nErro ao acessar a API do BC:")
        print(res.json())

list_dfs = []
for name, codigo in series.items():
    df = extrair_serie(codigo, name)
    list_dfs.append(df)

df_final = pd.concat(list_dfs)
print(df_final.shape)
print(df_final['indicador'].value_counts())

# df_final.to_sql("raw_indicadores_bcb", engine, if_exists='replace', index=False)

# transforma a tabela em CSV

# df_final.to_csv('./extract/data/indicadores_bcb.csv', index=False)
