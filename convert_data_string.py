import pandas as pd
from datetime import datetime as dtt
import os

def converte_para_texto():
    # Supondo que 'DATA E HORA' seja a coluna que contém o tempo em formato Unix
    df = pd.read_excel("Dados.xlsx")
    df.to_json("Dados.json")
    df['DATA E HORA']=df['DATA E HORA']/1000000000
    for i in df.index:
        timestamp = df.at[i, "DATA E HORA"] 
        datetime_obj = dtt.fromtimestamp(timestamp)
        formatted_time = datetime_obj.strftime('%m/%d/%Y %H:%M')
        df.at[i, "DATA E HORA"] = formatted_time
        print(df.at[i, "DATA E HORA"])

    df.to_json("Dados.json")
converte_para_texto()

def converte_para_ns():
    df = pd.read_json("Dados.json")

    df['DATA ms'] = pd.to_datetime(df['DATA E HORA'], format='%m/%d/%Y %H:%M').astype('int64') #tranforma em nano segundo

    print(df['DATA ms'])
    df.to_json("oi.json")


#converte_para_ns()