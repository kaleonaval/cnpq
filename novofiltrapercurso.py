import pandas as pd
from datetime import datetime 
from datetime import datetime as dtt
import time as tt
from tkinter import filedialog
import matplotlib.pyplot as plt
from datetime import datetime as dtt
import numpy as np
import matplotlib.image as mpimg
import statistics


def verifica_quadrado(limites,x,y):
    i=0
    for limite in limites:
        xi=limite[0][0]
        xf=limite[0][1]
        yi=limite[1][0]
        yf=limite[1][1]

        if xi <= x <=xf:
                if yi<=y<=yf:
                    return i
        i+=1
    return 55

def gera_percu(inicio,fim):
    perc=[inicio,fim]
    points=[]

    dados_excel = pd.read_excel("pontos.xlsx")
    points=[]
    for i in dados_excel.index:
            lo_f=dados_excel.at[i,"LON"]
            la_f=dados_excel.at[i,"LAT"]
            points.append((lo_f,la_f))

    lado_ori=0.10
    limites=[]
    tot=len(points)
    i=0
    #background_img = #plt.imread("mapa_base.png")
    #plt.imshow(background_img, aspect='auto',extent=[-45.4,-38.6,-26.2,-21.8])

    for point in points:
        if i==0:
            lado=lado_ori#+0.09
        else:
            lado=lado_ori
        xi = point[0] - lado 
        xf = point[0] + lado 
        yi = point[1] - lado 
        yf = point[1] + lado 
        limx=xi,xf
        limy=yi,yf
        limites.append((limx,limy))
        i+=1
    '''
    def checa_limites(lon,lat):
        i=0
        for lim in limites:
            xi,xf=lim[0]
            yi,yf=lim[1]
            if xi < lon < xf:
                if yi < lat < yf:
                    return (i)
            i+=1
            
        return 55
    dados=pd.read_json("dados.json")
    for i in dados.index:
        lon=dados.at[i,"LON"]
        lat=dados.at[i,"LAT"]
        ponto=checa_limites(lon,lat)
        dados.at[i,"LOCAL"]=ponto

    dados.to_json("dados.json",index=False)
    '''
    filtro=pd.read_json("dados.json")
    #filtro.to_csv("teste.csv")
    #filtro.reset_index(drop=True, inplace=True)
    tempos=[]
    current_list=[]
    percursos=[]
    tempo_viagem=[]
    current_percurso=[]
    erro_i=0
    erro_f=0
    for i in filtro.index:
        data=filtro.at[i,'DATA ms']
        local=filtro.at[i,"LOCAL"]
        if local == 55:

                if len(current_list)==1:
                    
                    list_inicio=[]
                    for t in range(0,8):
                        try:
                            loci=filtro.at[i-t,"LOCAL"] #10 pontos anteriores para saber a origem.
                        except:
                             loci=filtro.at[i,"LOCAL"]
                        list_inicio.append(loci)
                    inicio=statistics.mode(list_inicio) # moda dos 10 pontos
                    if inicio!=55:
                        current_percurso.append(inicio)
                    else:
                        current_list=[]
                current_list.append(data)
                

        else:
                if len(current_list)>5:
                    list_fim=[]
                    try:
                        for t in range(0,8):
                            loci=filtro.at[i+t,"LOCAL"] #10 pontos superiores para saber a origem.
                            list_fim.append(loci)
                        fim=statistics.mode(list_fim) # moda dos 10 pontos
                    except:
                        fim=55
                    if fim != 55:
                        if fim != inicio:
                            data_inicio=current_list[0]
                            
                            datetime_obj = dtt.fromtimestamp(data_inicio/ 1000000000)
                            data_inicio= datetime_obj.strftime('%m/%d/%Y %H:%M')
                            data_final=current_list[-1]
                            datetime_obj = dtt.fromtimestamp(data_final/ 1000000000)
                            data_final= datetime_obj.strftime('%m/%d/%Y %H:%M')
                            media_tempo=(current_list[-1]-current_list[0])/((6e+10)*60)
                            if 2< media_tempo < 30:
                                current_percurso.append(fim)
                                print(f"Inseriu percurso {current_percurso} com tempo {round(media_tempo,1)}. Data inicio = {data_inicio}. Data final = {data_final}")
                                percursos.append(current_percurso)
                                tempos.append(current_list)
                                tempo_viagem.append(media_tempo)

                                current_percurso=[]
                                current_list=[]
                                erro_f,erro_f=0,0
                            else:
                                current_percurso=[]
                                current_list=[]


    lista_dataframes = []
    tempo_viagem_perc=[]
    i=0
    for lista_indices in tempos:
        if percursos[i][0] == int(perc[0]):
            if percursos[i][1]==int(perc[1]):
                df_temp = filtro[filtro['DATA ms'].isin(lista_indices)]
                lista_dataframes.append(df_temp)
                tempo_viagem_perc.append(tempo_viagem[i])
        i+=1

    consumo_1=[]
    consumo_2=[]
    media_2=[]
    i=0
    for data_frame in lista_dataframes:
        total_data1=0
        total_data2=0
        data_frame.reset_index(drop=True, inplace=True)
        for index in data_frame.index:
                total_data1+=data_frame.at[index,"E1_CONSUMO_GH"]
                total_data2+=data_frame.at[index,"E2_CONSUMO_GH"]
                

        media_consumo1=total_data1*tempo_viagem_perc[i]
        media_consumo2=total_data2*tempo_viagem_perc[i]
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


    tempo,motor1,motor2,tempo_viagem=x,y1,y2,tempo_viagem_perc
    return tempo,motor1,motor2,tempo_viagem





def definir_percursos(dados):
    filtro=dados
    points=[]

    dados_excel = pd.read_excel("pontos.xlsx")
    points=[]
    for i in dados_excel.index:
            lo_f=dados_excel.at[i,"LON"]
            la_f=dados_excel.at[i,"LAT"]
            points.append((lo_f,la_f))

    lado_ori=0.10
    limites=[]
    tot=len(points)
    i=0
    #background_img = #plt.imread("mapa_base.png")
    #plt.imshow(background_img, aspect='auto',extent=[-45.4,-38.6,-26.2,-21.8])

    for point in points:
        if i==0:
            lado=lado_ori#+0.09
        else:
            lado=lado_ori
        xi = point[0] - lado 
        xf = point[0] + lado 
        yi = point[1] - lado 
        yf = point[1] + lado 
        limx=xi,xf
        limy=yi,yf
        limites.append((limx,limy))
        i+=1

    tempos=[]
    current_list=[]
    percursos=[]
    tempo_viagem=[]
    current_percurso=[]
    erro_i=0
    erro_f=0
    for i in filtro.index:
        data=filtro.at[i,'DATA ms']
        local=filtro.at[i,"LOCAL"]
        if local == 55:

                if len(current_list)==1:
                    
                    list_inicio=[]
                    for t in range(0,8):
                        try:
                            loci=filtro.at[i-t,"LOCAL"] #10 pontos anteriores para saber a origem.
                        except:
                             loci=filtro.at[i,"LOCAL"]
                        list_inicio.append(loci)
                    inicio=statistics.mode(list_inicio) # moda dos 10 pontos
                    if inicio!=55:
                        current_percurso.append(inicio)
                    else:
                        current_list=[]
                current_list.append(data)
                

        else:
                if len(current_list)>5:
                    list_fim=[]
                    try:
                        for t in range(0,8):
                            loci=filtro.at[i+t,"LOCAL"] #10 pontos superiores para saber a origem.
                            list_fim.append(loci)
                        fim=statistics.mode(list_fim) # moda dos 10 pontos
                    except:
                        fim=55
                    if fim != 55:
                        if fim != inicio:
                            data_inicio=current_list[0]
                            
                            datetime_obj = dtt.fromtimestamp(data_inicio/ 1000000000)
                            data_inicio= datetime_obj.strftime('%m/%d/%Y %H:%M')
                            data_final=current_list[-1]
                            datetime_obj = dtt.fromtimestamp(data_final/ 1000000000)
                            data_final= datetime_obj.strftime('%m/%d/%Y %H:%M')
                            media_tempo=(current_list[-1]-current_list[0])/((6e+10)*60)
                            if 2< media_tempo < 30:
                                current_percurso.append(fim)
                                print(f"Inseriu percurso {current_percurso} com tempo {round(media_tempo,1)}. Data inicio = {data_inicio}. Data final = {data_final}")
                                percursos.append(current_percurso)
                                tempos.append(current_list)
                                tempo_viagem.append(media_tempo)

                                current_percurso=[]
                                current_list=[]
                                erro_f,erro_f=0,0
                            else:
                                current_percurso=[]
                                current_list=[]


    i=0
    while i <len(tempos):
        j=0
        while j < len(tempos[i]):
            cur_temp=tempos[i][j]
            cur_perc=percursos[i]
            valorperc=f'{int(cur_perc[0])}--{int(cur_perc[1])}'
            filtro.loc[filtro["DATA ms"]==cur_temp,'PERCURSO']=valorperc
            if cur_perc[0]==0:
                 filtro.loc[filtro["DATA ms"]==cur_temp,'ROTA']=2
            else:
                 filtro.loc[filtro["DATA ms"]==cur_temp,'ROTA']=1
                 
                 
            j+=1
        i+=1


    return filtro 





class atualiza_paradas:
    def __init__(self,filtro) :
        self.filtro=filtro
        self.dados_excel = pd.read_excel("pontos.xlsx")
        self.points=[]
        for i in self.dados_excel.index:
                lo_f=self.dados_excel.at[i,"LON"]
                la_f=self.dados_excel.at[i,"LAT"]
                self.points.append((lo_f,la_f))
        
        self.main()


    def limites_iniciais(self):
        lado=0.10
        self.limites=[]
        i=0
        for point in self.points:
            if i==0:
                lado=lado+0.09
            else:
                lado=lado
            xi = point[0] - lado 
            xf = point[0] + lado 
            yi = point[1] - lado 
            yf = point[1] + lado 
            limx=xi,xf
            limy=yi,yf
            self.limites.append((limx,limy))
            i+=1





    def faz_quadrados(self):
        lado=0.10
        self.limites=[]
        i=0
        #background_img = #plt.imread("mapa_base.png")
        ##plt.imshow(background_img, aspect='auto',extent=[-45.4,-38.6,-26.2,-21.8])

        for point in self.points:
            xi = point[0] - lado 
            xf = point[0] + lado 
            yi = point[1] - lado 
            yf = point[1] + lado 
            xlm=[xi,xf,xf,xf,xf,xi,xi,xi]
            ylm=[yi,yi,yi,yf,yf,yf,yf,yi]
            ##plt.plot(xlm,ylm)
            ##plt.scatter(point[0],point[1])
            ##plt.text(point[0], point[1], str(i), fontsize=12, ha='center', va='center')
            limx=xi,xf
            limy=yi,yf
            self.limites.append((limx,limy))
            i+=1



    def main(self):    
        lado=0.10
        self.novos_pontos=[]
        self.limites_iniciais()
        lim_inicio=len(self.points)
        print(f"limite inicial: {len(self.limites)}")
       
        filtro=self.filtro
        def adiciona_limite(lon,lat): # adiciona limite para os pontos que não estão no limite ou não existe limite para eles
            self.points.append((lon,lat)) 
            for point in self.points:
                xi = point[0] - lado 
                xf = point[0] + lado 
                yi = point[1] - lado 
                yf = point[1] + lado 
                limx=xi,xf
                limy=yi,yf
                self.limites.append((limx,limy))
                print("Adicionou um novo ")

        def checa_limites(lon,lat):
            i=0
            for lim in self.limites:
                xi,xf=lim[0]
                yi,yf=lim[1]
                if xi < lon < xf:
                    if yi < lat < yf:
                        return (i,True)
                i+=1
                
            return (10000,False)


        filtro=filtro[filtro["VESSEL_KNOTS"]<2]
        x=[]
        y=[]
        c=[]
        for index in filtro.index:
            lat=round(filtro.at[index,"LAT"],2)
            lon=round(filtro.at[index,"LON"],2)
            r=checa_limites(lon,lat)
            if r[1]:
                color="blue"
            else:
                adiciona_limite(lon,lat)
                color="red"

            x.append(lon)
            y.append(lat)
            c.append(color)

        self.faz_quadrados()
        #plt.scatter(x,y,c=c)
        ##plt.show()
        
        dic = {}
        for index in filtro.index:
            lat = round(filtro.at[index, "LAT"], 2)
            lon = round(filtro.at[index, "LON"], 2)
            r = checa_limites(lon, lat)
            # Verifica se a chave já existe no dicionário
            if f'{r[0]}' not in dic:
                # Se não existir, inicializa com o valor 1
                dic[f'{r[0]}'] = 1
            else:
                # Se já existir, incrementa o valor existente
                dic[f'{r[0]}'] += 1

        indices_retirar=[]
        for ind,value in dic.items():
            if value < 10 and ind != 10000 and int(ind)>lim_inicio:
                indices_retirar.append(int(ind))

        indices_retirar.sort(reverse=True)
        for ind in indices_retirar:
            if ind < len(self.points):
                self.points.pop(ind)

        print(f"limite final: {len(self.points)}")
        i=0
        for point in self.points:
            xi = point[0] - lado 
            xf = point[0] + lado 
            yi = point[1] - lado 
            yf = point[1] + lado 
            xlm=[xi,xf,xf,xf,xf,xi,xi,xi]
            ylm=[yi,yi,yi,yf,yf,yf,yf,yi]
            #plt.plot(xlm,ylm)
            #plt.scatter(point[0],point[1])
            limx=xi,xf
            limy=yi,yf
            self.limites.append((limx,limy))
            i+=1
        #plt.show(block=False)

        self.completatabela()

    def completatabela(self):
        dataframe=pd.DataFrame()


        lat=[]
        lon=[]
        p=[]
        for i,e in enumerate(self.points):
            print(self.points[i][0])
            lon.append(self.points[i][0])
            lat.append(self.points[i][1])
            p.append(i)
            i+=1


        dataframe["LAT"]=lat
        dataframe["LON"]=lon
        dataframe["PONTO"]=p

        dataframe.to_excel("pontos.xlsx")




#dados=pd.read_json("Dados.json")

#gera_percu(0,4)
