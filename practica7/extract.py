
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date

#Empresas que se van a consultar
tickers=["NVDA","TSLA","MSFT","AMZN","AMD","INTC"]
#Datos de devolucion
raw_dfs={}
#Fecha
today=date.today()
today.strftime("%y-%m-%d")

#Datos desde NASDAQ

for ticker in tickers:
    tk = yf.Ticker(ticker)
    raw_df = pd.DataFrame(tk.history(period='1d'))
    #Transforma los strings a minusculas
    raw_df.columns=raw_df.columns.str.lower()
    #Elegir columnas que usaremos
    raw_df=raw_df[['open', 'high', 'low', 'close']]
    #Agrega inrofacion al diccionario
    raw_dfs[ticker]=raw_df


#print(raw_dfs["NVDA"])


#Datos de BTC
import requests
#consulta a la api
response = requests.get('https://api.coinbase.com/v2/prices/spot?currency=USD')
#Formato json
btc_raw = response.json()
#Filtramos la respuesta
btc_raw=float(btc_raw['data']['amount'])
#Index con fechas
btc_index=pd.to_datetime([today])
#diccionario con la resouesta de la api
btc_dic={"btc_usd":btc_raw}
btc_raw=pd.DataFrame(btc_dic,index=btc_index)

raw_dfs["btc_usd"]=btc_raw
#print(raw_dfs)

