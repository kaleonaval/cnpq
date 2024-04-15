import pandas as pd
from datetime import datetime 
import time
from tkinter import filedialog

start_time=time.strftime("%m/%d/%y %H:%M:%S", time.localtime())
f = "%m/%d/%y %H:%M:%S"

oi=pd.read_parquet("Dados.parquet")
#filtro=oi.loc[oi['VESSEL_KNOTS']<4]
filtro=oi
filtro=filtro.loc[filtro['PERCURSO']==3]
print(filtro['DIREÇÃO NAVIO'])
filtro=filtro.loc[filtro['ROTA']==2]
filtro.to_parquet("just_speed.parquet")
print("Fim")