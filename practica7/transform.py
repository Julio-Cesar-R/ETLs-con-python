import os
from extract import raw_dfs,tickers,today
import pandas as pd
import numpy as np

raw_dfs=raw_dfs.copy()
tickers=tickers.copy()
#Ingenieria de caracteristicas

for ticker in tickers:
    df= raw_dfs[ticker]
    df["dif_aper_cierre"]=df["open"]-df["close"]
    df["rango_dia"]=df["high"]-df["low"]
    df["signo_dia"]=np.where(df["dif_aper_cierre"]>0.0,"+",np.where(df["dif_aper_cierre"]<0.0,"-","0"))

    df=df[["close","dif_aper_cierre","rango_dia","signo_dia"]]
    df.columns=map(lambda x:ticker + "_"+ x, df.columns.to_list())
    raw_dfs[ticker]= df

print("----------------------------------------")
print(raw_dfs["NVDA"])

#Agregado
df_list=raw_dfs.values()
tablon=pd.concat(df_list,axis=1)

print(tablon)












