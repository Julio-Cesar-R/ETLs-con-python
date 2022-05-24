from prefect import Flow, task
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date



#Extraccion yfinance +API coinbase
@task
def extract(tickers,today):
    #Datos de devolucion
    raw_dfs={}
    #Datos desde NASDAQ
    print("Extrayendo la informacion de los tickers")
    for ticker in tickers:
        tk = yf.Ticker(ticker)
        raw_df = pd.DataFrame(tk.history(period='1d'))
        #Transforma los strings a minusculas
        raw_df.columns=raw_df.columns.str.lower()
        #Elegir columnas que usaremos
        raw_df=raw_df[['open', 'high', 'low', 'close']]
        #Agrega inrofacion al diccionario
        raw_dfs[ticker]=raw_df
    print("Extraccion exitosa de los tickers")

    #Datos de BTC
    import requests
    #consulta a la api
    print("Iniciando consulta a la api btc")
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
    print("Consulta a la api btc exitosa")
    return raw_dfs
    
    

#Transformacion
@task
def transform(raw_dfs,tickers):
    #Ingenieria de caracteristicas
    for ticker in tickers:
        df= raw_dfs[ticker]
        df["dif_aper_cierre"]=df["open"]-df["close"]
        df["rango_dia"]=df["high"]-df["low"]
        df["signo_dia"]=np.where(df["dif_aper_cierre"]>0.0,"+",np.where(df["dif_aper_cierre"]<0.0,"-","0"))

        df=df[["close","dif_aper_cierre","rango_dia","signo_dia"]]
        df.columns=map(lambda x:ticker + "_"+ x, df.columns.to_list())
        raw_dfs[ticker]= df

    #Agregado
    df_list=raw_dfs.values()
    tablon=pd.concat(df_list,axis=1)
    return tablon

#Carga
@task
def load(tablon):
    print(tablon)


with Flow("ETL Caso") as flow:
    #Empresas que se van a consultar
    tickers=["NVDA","TSLA","MSFT","AMZN","AMD","INTC"]
    #Fecha
    today=date.today()
    today.strftime("%y-%m-%d")
    
    raw_dfs=extract(tickers,today)
    tablon=transform(raw_dfs,tickers)
    load(tablon)
    
flow.run()