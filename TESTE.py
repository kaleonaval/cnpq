import math
import pandas as pd


d=pd.read_json("Dados_Tratados.json")
d.to_csv("Dados.csv")

def calcular_angulo(xis, yis, xf, yf):
    # Calculando as diferenças entre as coordenadas
    difx = xf - xis
    dify = yf - yis
    
    if dify>=0:
        if difx>=0:
            tetha=math.degrees(math.atan(dify/difx))

    if difx<=0:
        if dify>=0:
            tetha=-math.degrees(math.atan(dify/difx))+90
        
    if difx>=0:
        if dify<=0:
            tetha=-math.degrees(math.atan(difx/dify))+270

    if difx<=0:
            if dify<=0:
                tetha=math.degrees(math.atan(dify/difx))+180

    return tetha

# Exemplo de uso
import pandas as pd
data=pd.read_excel("just_speed.xlsx")
for i in data.index:
    
    xf=data.at[i,"LON"]
    yf=data.at[i,"LAT"]
    try:
        xi=data.at[i-1,"LON"]
        yi=data.at[i-1,"LAT"]
    except:
        xi,yi=xf,yf

    print(calcular_angulo(xi,yi,xf,yf))

from PIL import Image

#imagem_png =Image.open("icones\ship.png").convert("RGBA").rotate(225,Image.NEAREST,expand=1)
#imagem_png.show()
