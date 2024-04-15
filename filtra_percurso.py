import pandas as pd
from datetime import datetime 
import time as tt
from tkinter import filedialog
import matplotlib.pyplot as plt
from datetime import datetime as dtt
import numpy as np

def gera_media_por_percurso(percurso,rota,titulo,data_frame):

    filtro=data_frame
    filtro=filtro.loc[filtro['PERCURSO']==percurso]
    filtro=filtro.loc[filtro['VESSEL_KNOTS']>7]
    if not rota=="TODOS":
        filtro=filtro.loc[filtro['ROTA']==rota] # 1 RUMO AO PORTO ; 2 RUMO A PLATAFORMA ; TODOS
    filtro.reset_index(drop=True, inplace=True)
    tempos=[]
    current_list=[]
    tempo_viagem=[]
    for i in filtro.index:
        try:
            tempo=filtro.at[i,'DATA ms']
            tempo_1=filtro.at[i+1,'DATA ms']
            dif=(tempo_1-tempo)/6e+10
            if dif<65:
                current_list.append(tempo)
                print(dif,filtro.at[i,"DATA E HORA"])
                
            else:

                primeiro_tempo=current_list[0]/6e+10
                ultimo_tempo=current_list[-1]/6e+10
                dif2=ultimo_tempo-primeiro_tempo
                dif2_h=dif2/((60))
                media_lista=dif2/len(current_list)

                if len(current_list)>=8:
                    if dif2_h>9: # precisa definir o tempo de cada percurso. Se o tempo médio for de 10h, entao colocar pelo menos 8. Fazer cálculo com base na distância da baia.
                        print(f" dif horas = {dif2_h}")
                        tempo_viagem.append(dif2_h)
                        tempos.append(current_list)


                current_list=[]

        
        except:
            print(f"erro {i}")
    print(len(tempos))
    print(len(tempo_viagem))
    lista_dataframes = []
    for lista_indices in tempos:
        df_temp = filtro[filtro['DATA ms'].isin(lista_indices)]
        lista_dataframes.append(df_temp)

    consumo_1=[]
    consumo_2=[]
    media_2=[]
    i=0
    for data_frame in lista_dataframes:
        media_consumo1=data_frame["E1_CONSUMO_GH"].mean()*tempo_viagem[i]
        media_consumo2=data_frame["E2_CONSUMO_GH"].mean()*tempo_viagem[i]
        time=data_frame['DATA ms'].mean()
        consumo_1.append((media_consumo1,time))
        consumo_2.append((media_consumo2,time))
        i+=1
    i=0
    for c in consumo_1:
        media_2.append((consumo_1[i][0]+consumo_2[i][0])/2) # [0] pq eu coloco o com appende (media,time) -- 0 pega média
        i+=1
    
    
    x=[dtt.fromtimestamp(time[1]/1000000000).strftime('%m/%d/%y') for time in consumo_1]
    y1=[con1[0] for con1 in consumo_1]
    y2=[con2[0] for con2 in consumo_2]
    fig, ax1 = plt.subplots()
    tempo,motor1,motor2,tempo_viagem=x,y1,y2,tempo_viagem
    return tempo,motor1,motor2,tempo_viagem

    ax2 = ax1.twinx()
    ax1.plot(x,y1)
    ax1.plot(x,y2)

    ax2.plot(x,tempo_viagem,c="red") # queria definir o intervalo desse no lado direito, separado. Dois intervalos y um na esquerda e outro na direira. 
    plt.xticks(rotation=90)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)
    ax1.set_ylim(0,8000000)
    ax2.set_ylabel('Tempo (horas)', color='red')
    ax1.set_ylabel('Consumo [g] MÉDIO POR VIAGEM', color='orange')
    ax2.legend(loc="best")



    plt.show()

#dados=pd.read_json("Dados.json")

#gera_media_por_percurso(percurso=4,rota=2,titulo="E2_CONSUMO_GH",data_frame=dados)