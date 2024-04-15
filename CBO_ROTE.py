import requests 
from PIL import Image
import matplotlib.colors as mcolors
import matplotlib as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import time
import requests
import numpy as np
from scipy import ndimage
import pandas as pd
import os

class rotas_mapas:
    def __init__(self):
        self.key='AIzaSyBx6k7cF00yNKyG0DDhcwQ0sFf5fcltWeM'
        self.font=ImageFont.truetype("ABeeZee-Regular.otf", 26)
        maps='roadmap', 'satellite', 'hybrid', 'terrain'
        self.map=maps[3]



    def gera_mapa_percursos(self,name_file="ll.png"):
        dados_excel = pd.read_excel("percursos.xlsx")
        points=[]
        origem = (-43.1, -22.8)
        points.append(origem)
        latitudes=[]
        longitudes=[]
        for i in dados_excel.index:
            try:
                lo_or=dados_excel.iloc[i+2,1]
                la_or=dados_excel.iloc[i+2,3]
                lo_f=dados_excel.iloc[i+2,2]
                la_f=dados_excel.iloc[i+2,4]
                latitudes.append(la_or)
                latitudes.append(la_f)
                longitudes.append(lo_or)
                longitudes.append(lo_f)
                points.append((la_f,lo_f))
                
            except:
                pass
        # Converter os dados em uma lista de tuplas (latitude, longitude)
        pontos = list(zip(latitudes, longitudes))

        # Converter a lista de pontos em uma string formatada para a URL
        waypoints = '|'.join([f"{lat},{lon}" for lat, lon in pontos])
        rotas = [pontos[i:i+2] for i in range(0, len(pontos), 2)]

        # Obter cores distintas da paleta Tab20
        cores_rgb = plt.cm.tab20(np.linspace(0, 1, len(rotas)))

        # Converter as cores para o formato hexadecimal
        cores_hex = [mcolors.rgb2hex(cor) for cor in cores_rgb]

        # Converter as cores para o formato correto para a URL
        cores_url = [f'0x{cor[1:]}' for cor in cores_hex]
        # Construir a URL do Google Maps Static API com as rotas e cores intercaladas

        width=int((-39-(-45))*90)
        height=int((-21+26.5)*100)
        width,height=620,440

        center_lat=((-26.5-21.5)/2)
        center_lon=((-45-39)/2)
        scale=2
        #plt.xlim([-45, -39])  # Defina limite_min_x e limite_max_x conforme necessário
        #plt.ylim([-26.5, -22.5])  # Defina limite_min_y e limite_max_y conforme necessário


        url_base = f"https://maps.googleapis.com/maps/api/staticmap?size={width}x{height}&center={center_lat},{center_lon}&zoom=7&scale={scale}&maptype={self.map}"
        url_path = '&'.join([f'path=color:{cor}|weight:4|{"|".join([f"{lat},{lon}" for lat, lon in rota])}' for cor, rota in zip(cores_url, rotas)])
        markers = "&".join([f"markers=color:red%7Clabel:{i}%7C{lat},{lon}" for i, (lat, lon) in enumerate(points)])

        url = f"{url_base}&{url_path}&{markers}&key={self.key}"


        print(url)
        response = requests.get(url)
        # Salvar a imagem do mapa em um arquivo
        with open(name_file, 'wb') as f:
            f.write(response.content)
        #Image.open(name_file).show()

#gera_mapa_percursos()

    def colocar_icone(self,fundo_frame,imagem,x,y,dir,rota,icone="icones/ship.png"):
        if rota==0:
            rota_text="PARADO"
        if rota==1:
            rota_text="RUMO AO RIO DE JANEIRO"
        if rota==2:
            rota_text="RUMO À PLATAFORMA"

        print(dir)
        imagem_principal = Image.open(fundo_frame).convert("RGBA")
        if dir==1000:
            dir=270
        imagem_png =Image.open(icone).convert("RGBA").rotate(dir,Image.NEAREST,expand=1)

        coordenada_x = x
        coordenada_y = y

        # Cole a imagem PNG na imagem principal nas coordenadas calculadas
        fundo_frame=Image.open(fundo_frame)
        draw=ImageDraw.Draw(fundo_frame)

        draw2=ImageDraw.Draw(imagem_principal)
    
        x=x+80
        y=y+40
        r=2

        draw.ellipse((x-r, y-r, x+r, y+r), fill="red")
        if dir==1000:
            rota_text=""
        
        text=f"CBO BIANCA \n {rota_text}"
        imagem_principal.paste(imagem_png, (coordenada_x, coordenada_y), imagem_png)
        draw2.text((x+40,y),text=text,fill="red",font=self.font)

        return imagem_principal,fundo_frame






    def gera_frames(self,dataframe,name_file="frames\Frame 0.png",lim_frames=200):
            # Chave da API do Google Maps (substitua pela sua chave)
            self.key = 'AIzaSyBx6k7cF00yNKyG0DDhcwQ0sFf5fcltWeM'

            # Carregar os dados do Excel
            dados_excel =dataframe

            latitudes=dados_excel["LAT"].to_list()
            longitudes=dados_excel["LON"].to_list()
            direcao=dados_excel["DIREÇÃO NAVIO"].to_list()
            rotas=dados_excel["ROTA"].to_list()
            center_lat=-24
            center_lon=-42
            
            largura=6.82
            altura=4.4
            #largura e altura de lat e lon, referente ao zoom 7 largura 620 e altura 440 em pixels 

            width,height=620,440

            center_lat=-24
            center_lon=-42

            scale=2
            #plt.xlim([-45, -39])  # Defina limite_min_x e limite_max_x conforme necessário
            #plt.ylim([-26.5, -22.5])  # Defina limite_min_y e limite_max_y conforme necessário
            arqs=os.listdir("Frames")
            for arq in arqs:
                arq=f"Frames\{arq}"
                os.remove(arq)

            arqs=os.listdir("Frame Fundos")
            for arq in arqs:
                arq=f"Frame Fundos\{arq}"
                os.remove(arq)
            '''
            try:
            
                url_base = f"https://maps.googleapis.com/maps/api/staticmap?size={width}x{height}&center={center_lat},{center_lon}&zoom=7&scale={scale}&maptype={self.map}"

                url = f"{url_base}&key={self.key}"
                response = requests.get(url)
                # Salvar a imagem do mapa em um arquivo
                with open(name_file, 'wb') as f:
                    f.write(response.content)
            except:
            '''
            name_file="mapa_base1.png"



            t_p=len(latitudes)
            new_lat=[]
            new_lon=[]
            new_dir=[]
            new_rota=[]
            total_retirar=t_p-lim_frames
            print(total_retirar,t_p,lim_frames)
            step=int(t_p/lim_frames)+1
            print(f"step {step}")
            if t_p>lim_frames:
                i=0
                while i<t_p:
                    new_lat.append(latitudes[i])
                    new_lon.append(longitudes[i])
                    new_dir.append(direcao[i])
                    new_rota.append(rotas[i])
                    i+=step
            else:
                new_dir=direcao
                new_lon=longitudes
                new_lat=latitudes
                new_rota=rotas


            print(f"Total frames = {len(new_dir)}")
            for i,lat in enumerate(new_lon):
                name_frame=f"frames\Frame {i}.png"
                fundo_frame=f"Frame Fundos\Fundo_frame {i}.png"
                old_fundo=f"Frame Fundos\Fundo_frame {i-1}.png"
                lat=new_lat[i]
                lon=new_lon[i]
                dir=new_dir[i]
                rota=new_rota[i]
                x=int((lon+45.1)*85*scale)
                y=int(440*scale)-int((lat+26.5)*100*scale)

                if i==0:
                    img,fundo=self.colocar_icone(name_file,name_file,x=x,y=y,dir=dir,rota=rota)
                else:
                    img,fundo=self.colocar_icone(old_fundo,name_file,x=x,y=y,dir=dir,rota=rota)

                #img.show()
                img.save(name_frame)
                fundo.save(fundo_frame)


    def gera_mapa_pontos(self,lon,lat,dir,rota,name="motores.png"):

            center_lat=-24
            center_lon=-42
            dir=dir
            width,height=620,440
            scale=2
            #plt.xlim([-45, -39])  # Defina limite_min_x e limite_max_x conforme necessário
            #plt.ylim([-26.5, -22.5])  # Defina limite_min_y e limite_max_y conforme necessário


            #url_base = f"https://maps.googleapis.com/maps/api/staticmap?size={width}x{height}&center={center_lat},{center_lon}&zoom=7&scale={scale}&maptype={self.map}"

            #url = f"{url_base}&key={self.key}"
            #response = requests.get(url)
            name_file="mapa_base.png"
            #with open(name, 'wb') as f:
            #    f.write(response.content)

            x=int((lon+45.1)*85*scale)
            y=int(440*scale)-int((lat+26.5)*100*scale)
            img,imgf=self.colocar_icone(fundo_frame=name_file,imagem=name_file,x=x,y=y,dir=dir,rota=rota)
            img.save(name)
            return name
    
#rotas_mapas().gera_frames(dataframe=pd.read_parquet("just_speed.parquet"),lim_frames=200)
#rotas_mapas().gera_mapa_pontos(lon=1,lat=1,dir=1,rota=1)