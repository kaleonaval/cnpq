
import matplotlib.pyplot as plt
import tkinter as tk
import openpyxl
import numpy as np 
import matplotlib.colors as mcolors
import matplotlib.image as mpimg
from CBO_ROTE import rotas_mapas
import pandas as pd


class percurso:
    def __init__(self,fig=None,ax=None,canvas=None,master=None,interface=False):
        self.interface=interface
        self.run=True
        self.rotas=rotas_mapas()
        self.canvasgraficoperc=canvas
        self.fig=fig
        self.ax=ax
        self.pontos=[]
        self.coeficientespercusos=[]
        self.interfacetrue()


    def calcular_coeficientes(self,x1, y1, x2, y2):
        # Calcular o coeficiente angular (inclinação da reta)
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1
        return a, b,x1,x2,y1,y2

    def verificar_entre(self, limite1,numero, limite2):
        limite_inf = min(limite1, limite2)
        limite_sup = max(limite1, limite2)
        return limite_inf <= numero <= limite_sup
    

        
    def interfacetrue(self):
        print("CHEGUEI AQUI ")
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

        for point in points:
            if i==0:
                lado=lado_ori#+0.09
            else:
                lado=lado_ori
            xi = point[0] - lado 
            xf = point[0] + lado 
            yi = point[1] - lado 
            yf = point[1] + lado 
            xlm=[xi,xf,xf,xf,xf,xi,xi,xi]
            ylm=[yi,yi,yi,yf,yf,yf,yf,yi]
            plt.plot(xlm,ylm)
            plt.scatter(point[0],point[1])
            plt.plot((point[0],-43.2),(point[1],-22.8))
            plt.text(point[0], point[1], str(i), fontsize=12, ha='center', va='center')
            limx=xi,xf
            limy=yi,yf
            limites.append((limx,limy))
            i+=1
            num_cores = 20
            center_lat=-24
            center_lon=-42
            
            largura=6.82
            altura=4.4
            xi=center_lon-largura/2
            xf=center_lon+largura/2
            yi=center_lat-altura/2
            yf=center_lat+altura/2
            background_img = mpimg.imread('mapa_base.png')
            
            
            # Exibir a imagem de fundo
            plt.imshow(background_img, extent=[xi-0.3, xf+0.3, yi, yf], aspect='auto')
            plt.title('Percursos')
            plt.xlabel('Longitude',fontsize=8)
            plt.ylabel('Latitude',fontsize=8)
            plt.legend(loc='center right',bbox_to_anchor=(1.25,0.5))
            
            # Limitar os intervalos dos eixos
            plt.xlim([xi, xf])  # Defina limite_min_x e limite_max_x conforme necessário
            plt.ylim([yi, yf])  # Defina limite_min_y e limite_max_y conforme necessário
            plt.subplots_adjust(right=0.8)
            plt.subplots_adjust(top=0.9)


