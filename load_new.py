from tkinter import filedialog
import pandas as pd
import math
from tkinter import messagebox
from analisepercurso import percurso
from novofiltrapercurso import definir_percursos,atualiza_paradas

class carregar:
    def __init__(self):

        pass
    def calcular_angulo(self,xis, yis, xf, yf):
        # Calculando as diferenças entre as coordenadas
        difx = xf - xis
        dify = yf - yis
        
        if dify>=0:
            if difx>=0:
                tetha=math.degrees(math.atan(dify/difx))

        if difx<=0:
            if dify>=0:
                tetha=-math.degrees(math.atan(difx/dify))+90
            
        if difx>=0:
            if dify<=0:
                tetha=-math.degrees(math.atan(difx/dify))+270

        if difx<=0:
                if dify<=0:
                    tetha=math.degrees(math.atan(dify/difx))+180

        return tetha
    

    def verifica_quadrado(self,x,y):
        i=0
        for limite in self.limites:
            xi=limite[0][0]
            xf=limite[0][1]
            yi=limite[1][0]
            yf=limite[1][1]
            if xi <= x <=xf:
                 if yi<=y<=yf:
                      return i

            i+=1
        return 0

    def carregar_dados(self):

        # Carregando os dados a partir do arquivo Excel
        filetypes = [("Excel files", "*.xlsx"),("Excel CSV",".csv")]
        try:
            dados=filedialog.askopenfilenames(filetypes=filetypes)
            print(dados)
        except:
            messagebox.showerror("Info","Dados não foram carregados")

        if dados=="":
            messagebox.showerror("Info","Dados não foram carregados")
            return 1
        
        #threading.Thread(target=self.telacarregando).start()
        type=dados[0][-4:]
        alldate=[]
        if type ==".csv":
            for date in dados:
                date=pd.read_csv(date)
                alldate.append(date)

        else:
            for date in dados:
                date=pd.read_excel(date)
                alldate.append(date)
                print(date)

        self.df = pd.concat(alldate, ignore_index=True)
        
    

        colunas=self.df.columns
        if "VESSEL_MPH" in colunas:
            self.df["VESSEL_KNOTS"]=self.df["VESSEL_MPH"]*0.868976
            messagebox.showinfo(title="hello",message="Doesen't exist VESSEL_KNOTS in data, a conversion was made to get a knots from mph.")
        atualiza_paradas(self.df)
        self.df_dadosnovos = pd.DataFrame((self.df.SIG_WAVE_HEIGHT_M,self.df.WIND_SPEED_M_PER_S,self.df.WIND_DIRECTION,self.df.TEMPERATURE_C,self.df.E1_M3PD,self.df.E1_S_GPC3,self.df.E2_M3PD,self.df.E2_S_GPC3,self.df.VESSEL_KNOTS,self.df.LAT,self.df.LON), index=["SIG_WAVE_HEIGHT_M","WIND_SPEED_M_PER_S","WIND_DIRECTION","TEMPERATURE_C","E1_M3PD","E1_S_GPC3","E2_M3PD","E2_S_GPC3","VESSEL_KNOTS","LAT","LON"]).T

        # Corrigindo latitude e longitude
        self.df_dadosnovos["LAT CORRIGIDA"] = round(self.df_dadosnovos["LAT"],4)
        self.df_dadosnovos["LON CORRIGIDA"] = round(self.df_dadosnovos["LON"],4)
    
        # Convertendo latitude e longitude para radianos
        self.df_dadosnovos["LAT RAD"] = self.df_dadosnovos["LAT"]*2*math.pi/360
        self.df_dadosnovos["LON RAD"] = self.df_dadosnovos["LON"]*2*math.pi/360

        # Criando coluna para identificação do percurso
        self.df_dadosnovos["PERCURSO"] = 0
        self.df_dadosnovos["DIST"] = 0
        self.df_dadosnovos["ROTA"] = 0
        # Separando a coluna de data e hora em duas
        df_datahora = self.df.iloc[:,0]
        df_hora =  df_datahora.str[-5:]

        # Incluindo as colunas de data e hora no dataframe
        self.df_dadosnovos["DATA E HORA"] = df_datahora     
        self.df_dadosnovos['DATA ms'] = pd.to_datetime(self.df_dadosnovos['DATA E HORA'], format='%m/%d/%Y %H:%M').astype('int64') #tranforma em nano segundo   


        # Incluindo as colunas de consumo (g/m3), consumo (g/h), potência, rotação, consumo total
        self.df_dadosnovos["E1_S_GPM3"] = 0
        self.df_dadosnovos["E1_CONSUMO_GH"] = 0
        self.df_dadosnovos["E1_POTÊNCIA_KW"] = 0
        self.df_dadosnovos["E1_ROTAÇÃO_RPM"] = 0
        self.df_dadosnovos["E2_S_GPM3"] = 0
        self.df_dadosnovos["E2_CONSUMO_GH"] = 0
        self.df_dadosnovos["E2_POTÊNCIA_KW"] = 0
        self.df_dadosnovos["E2_ROTAÇÃO_RPM"] = 0

        # Calculando E1_S_GPM3
        self.df_dadosnovos["E1_S_GPM3"] = self.df_dadosnovos["E1_S_GPC3"]*1000000
        
        # Calculando E1_CONSUMO_GH
        self.df_dadosnovos["E1_CONSUMO_GH"] = (self.df_dadosnovos["E1_S_GPM3"]*self.df_dadosnovos["E1_M3PD"])/24

        # Calculando E1_POTÊNCIA_KW
        self.df_dadosnovos["E1_POTÊNCIA_KW"] = ((-9)*(10**(-10))*(self.df_dadosnovos["E1_CONSUMO_GH"]**2))+(0.0058*self.df_dadosnovos["E1_CONSUMO_GH"])-119.5

        # Calculando E1_ROTAÇÃO_RPM
        self.df_dadosnovos["E1_ROTAÇÃO_RPM"] = ((-2)*(10**(-9))*(self.df_dadosnovos["E1_CONSUMO_GH"]**2))+(0.0024*self.df_dadosnovos["E1_CONSUMO_GH"])+251.69

        # Calculando E2_S_GPM3
        self.df_dadosnovos["E2_S_GPM3"] = self.df_dadosnovos["E2_S_GPC3"]*1000000
        
        # Calculando E2_CONSUMO_GH
        self.df_dadosnovos["E2_CONSUMO_GH"] = (self.df_dadosnovos["E2_S_GPM3"]*self.df_dadosnovos["E2_M3PD"])/24

        # Calculando E2_POTÊNCIA_KW
        self.df_dadosnovos["E2_POTÊNCIA_KW"] = ((-9)*(10**(-10))*(self.df_dadosnovos["E2_CONSUMO_GH"]**2))+(0.0058*self.df_dadosnovos["E2_CONSUMO_GH"])-119.5

        # Calculando E2_ROTAÇÃO_RPM
        self.df_dadosnovos["E2_ROTAÇÃO_RPM"] = ((-2)*(10**(-9))*(self.df_dadosnovos["E2_CONSUMO_GH"]**2))+(0.0024*self.df_dadosnovos["E2_CONSUMO_GH"])+251.69

        # Incluindo as colunas de data e hora no dataframe    
        #self.df_dadosnovos["DATA"] = df_data
        self.df_dadosnovos["HORA"] = df_hora




        #aba para verificar limites quadrados dos percursos se esta no porto ou plataforma
        points=[]
        dados_excel = pd.read_excel("pontos.xlsx")
        points=[]
        for i in dados_excel.index:
                lo_f=dados_excel.at[i,"LON"]
                la_f=dados_excel.at[i,"LAT"]
                points.append((lo_f,la_f))

        lado=0.10
        self.limites=[]
        tot=len(points)
        i=0
        for point in points:
            if i==0:
                lado+=0.10
            xi = point[0] - lado 
            xf = point[0] + lado 
            yi = point[1] - lado 
            yf = point[1] + lado 
            limx=xi,xf
            limy=yi,yf
            self.limites.append((limx,limy))
            i+=1


        origem=(-43.1, -22.8)
        percobj=percurso(interface=False)
        for i in self.df_dadosnovos.index:
            try:
                self.df_dadosnovos.at[i-1,"DIST"] = (2*6378.137*math.asin(math.sqrt((math.sin((self.df_dadosnovos.at[i-1,"LAT"]-self.df_dadosnovos.at[i-2,"LAT"])/2)**2)+(math.cos(self.df_dadosnovos.at[i-2,"LAT"])*math.cos(self.df_dadosnovos.at[i-1,"LAT"])*(math.sin((self.df_dadosnovos.at[i-1,"LON"]-self.df_dadosnovos.at[i-2,"LON"])/2))**2))))/1.852
            
            except:
                print('erro dist')
                pass

            lat,long=self.df_dadosnovos.at[i,"LAT"] ,self.df_dadosnovos.at[i,"LON"] 
            try:
                lat_ant,long_ant=self.df_dadosnovos.at[i-1,"LAT"] ,self.df_dadosnovos.at[i-1,"LON"] 
            except:
                lat_ant,long_ant=lat,long
                print("erro lat long")

            yis,xis,yf,xf=lat_ant,long_ant,lat,long
            dx1=xis-origem[0]
            dy1=yis-origem[1]
            dx2=xf-origem[0]
            dy2=yf-origem[1]
        
            dist1=(dx1**2+dy1**2)**(1/2)
            dist2=(dx2**2+dy2**2)**(1/2)

            xf=self.df_dadosnovos.at[i,"LON"]
            yf=self.df_dadosnovos.at[i,"LAT"]
            try:
                xi=self.df_dadosnovos.at[i-1,"LON"]
                yi=self.df_dadosnovos.at[i-1,"LAT"]
            except:
                xi,yi=xf,yf

            tetha=self.calcular_angulo(xi,yi,xf,yf)

            
            if self.df_dadosnovos.at[i,'VESSEL_KNOTS']<1:
                tetha=0
                        
            self.df_dadosnovos.at[i,"DIREÇÃO NAVIO"]=tetha



            def checa_limites(lon,lat):
                i=0
                for lim in self.limites:
                    xi,xf=lim[0]
                    yi,yf=lim[1]
                    if xi < lon < xf:
                        if yi < lat < yf:
                            return (i)
                    i+=1
                    
                return 55


            ponto=checa_limites(long,lat)
            self.df_dadosnovos.at[i,"LOCAL"]=ponto
            if ponto != 55:
                self.df_dadosnovos.at[i,"PERCURSO"] = f'{ponto}--{ponto}'
                self.df_dadosnovos.at[i,'ROTA'] = 0   #PARADO
            else:
                self.df_dadosnovos.at[i,"PERCURSO"] = f'undefined' 

        

            if i == 0:
                self.df_dadosnovos.at[i,"DLA"] = 0
            else:
                self.df_dadosnovos.at[i,"DLA"] = self.df_dadosnovos.at[i,"LAT"]-self.df_dadosnovos.at[i-1,"LAT"]
        

            if i == 0:
                self.df_dadosnovos.at[i,"DLO"] = 0
            else:
                self.df_dadosnovos.at[i,"DLO"] = self.df_dadosnovos.at[i,"LON"]-self.df_dadosnovos.at[i-1,"LON"]
        

            if i == 0:
                self.df_dadosnovos.at[i,"a"] = 0
            else:
                if self.df_dadosnovos.at[i,"DLA"] == 0 or self.df_dadosnovos.at[i,"DLO"] == 0:
                    self.df_dadosnovos.at[i,"a"] = 0
                elif self.df_dadosnovos.at[i,"DLA"] >= 0 and self.df_dadosnovos.at[i,"DLO"] >= 0:
                    self.df_dadosnovos.at[i,"a"] = math.degrees(math.atan(self.df_dadosnovos.at[i,"DLA"]/self.df_dadosnovos.at[i,"DLO"]))
                elif self.df_dadosnovos.at[i,"DLA"] >= 0 and self.df_dadosnovos.at[i,"DLO"] < 0:
                    self.df_dadosnovos.at[i,"a"] = math.degrees(math.atan(self.df_dadosnovos.at[i,"DLO"]/self.df_dadosnovos.at[i,"DLA"]))
                elif self.df_dadosnovos.at[i,"DLA"] < 0 and self.df_dadosnovos.at[i,"DLO"] < 0:
                    self.df_dadosnovos.at[i,"a"] = math.degrees(math.atan(self.df_dadosnovos.at[i,"DLA"]/self.df_dadosnovos.at[i,"DLO"]))
                else:
                    self.df_dadosnovos.at[i,"a"] = math.degrees(math.atan(self.df_dadosnovos.at[i,"DLO"]/self.df_dadosnovos.at[i,"DLA"]))


            if i == 0:
                self.df_dadosnovos.at[i,"B"] = 0
            else:
                self.df_dadosnovos.at[i,"B"] = 180 - 90 - self.df_dadosnovos.at[i,"a"]
        

            if i == 0:
                self.df_dadosnovos.at[i,"RV"] = 0
            else:
                if self.df_dadosnovos.at[i,"DLA"] >= 0 and self.df_dadosnovos.at[i,"DLO"] >= 0:
                    self.df_dadosnovos.at[i,"RV"] = 90 - self.df_dadosnovos.at[i,"a"]
                elif self.df_dadosnovos.at[i,"DLA"] >= 0 and self.df_dadosnovos.at[i,"DLO"] < 0:
                    self.df_dadosnovos.at[i,"RV"] = 360 + self.df_dadosnovos.at[i,"a"]
                elif self.df_dadosnovos.at[i,"DLA"] < 0 and self.df_dadosnovos.at[i,"DLO"] < 0:
                    self.df_dadosnovos.at[i,"RV"] = 180 + (90 - self.df_dadosnovos.at[i,"a"])
                else:
                    self.df_dadosnovos.at[i,"RV"] = 180 + self.df_dadosnovos.at[i,"a"]


            if i == 0:
                self.df_dadosnovos.at[i,"RM"] = 0
            else:
                self.df_dadosnovos.at[i,"RM"] = self.df_dadosnovos.at[i,"RV"] + 21
        
            self.df_dadosnovos["REL_WIND_DIRECTION"] = self.df_dadosnovos.at[i,"WIND_DIRECTION"] - self.df_dadosnovos.at[i,"RV"]

            if -90 <= self.df_dadosnovos.at[i,"REL_WIND_DIRECTION"] <= 90:
                self.df_dadosnovos.at[i,"WIND_SPEED_M_PER_S_COR"] = self.df_dadosnovos.at[i,"WIND_SPEED_M_PER_S"]
            else:
                self.df_dadosnovos.at[i,"WIND_SPEED_M_PER_S_COR"] = 0

            if -90 <= self.df_dadosnovos.at[i,"WIND_SPEED_M_PER_S_COR"] <= 90:
                self.df_dadosnovos.at[i,"SIG_WAVE_HEIGHT_M_COR"] = self.df_dadosnovos.at[i,"SIG_WAVE_HEIGHT_M"]
            else:
                self.df_dadosnovos.at[i,"SIG_WAVE_HEIGHT_M_COR"] = 0



            self.df_dadosnovos["E1_E2_CONSUMO_GH"] = self.df_dadosnovos.at[i,"E1_CONSUMO_GH"] + self.df_dadosnovos.at[i,"E2_CONSUMO_GH"]

        self.df_dadosnovos=definir_percursos(self.df_dadosnovos)

        self.df_dadosnovos=self.df_dadosnovos.drop_duplicates(subset="DATA E HORA",keep="first")
        self.df_dadosnovos.sort_values(by='DATA ms')
        self.df_dadosnovos.to_json('Dados_Tratados.json')
        #self.df_dadosnovos.to_json("Dados.json")
        messagebox.showinfo(title='Carregamento de dados finalizado',message='Os dados foram carregados com sucesso.')
        return 2

#carregar().carregar_dados()
    
#d=pd.read_excel("Dados_tratados.xlsx")
#d.to_json("Dados.json")
#print("fim")