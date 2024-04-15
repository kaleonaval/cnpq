
from tela_carregamento import carregamento
import threading
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tendencias import tendencias
from load_new import carregar
import datetime
from datetime import datetime as dt
from PIL import Image
from CBO_ROTE import rotas_mapas
from novofiltrapercurso import gera_percu
obj=carregamento()
threading.Thread(target=obj.carrega_interface).start()
import tkinter as tk

import math
import numpy as np
import matplotlib.pyplot as plt

from datetime import date
import pandas as pd
obj.tela_carregamento(20,0.5)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
obj.tela_carregamento(50,1)
import os
from tkinter import filedialog
from tkcalendar import Calendar
import openpyxl
from openpyxl.styles import PatternFill
import time 
from analisepercurso import percurso
from addplot import criagrafico
threading.Thread(target=obj.tela_carregamento,args=(99,1.2)).start()
#from redeneural import rede
from PIL import Image, ImageTk



class main():
    def __init__(self,master):
        #print("cheguei aqui 2")
        self.master=master
        self.master.overrideredirect(False)
        self.master.attributes('-topmost',False)
        #print("cheguei aqui 3")
        self.figsmotores=[]
        self.imagens_fundo=[]
        self.titulos_number=[]
        self.calendario_ativado=False
        self.master.title('PROJETO CNPQ EFICIÊNCIA ENERGÉTICA')
        self.master.geometry('900x585+0+0')
        self.largura_tela = self.master.winfo_screenwidth()
        self.altura_tela = self.master.winfo_screenheight()
        self.escalax=1920/self.largura_tela
        self.escalay=1080/self.largura_tela
        self.cor_fundo="#555555"
        self.master.option_add('*background',self.cor_fundo)
        self.master.option_add('*foreground','white')


        self.framegraficoativotendencia=False
        self.framegraficoativo=False
        self.framegraficoativoperc=False
        self.gerougrafico=False
        self.escala_x_grafico=10
        self.datas_list=[]
        self.mapas_rotas=rotas_mapas()
        self.carregaricones()
        self.gerainterface()
        self.theread_abre_dados_tratados()
       # self.master.mainloop()
        
    def theread_abre_dados_tratados(self):
        self.abre_dados_tratados()
        #inicia.start()

    def theread_abre_dados_novos(self):
        inicia=threading.Thread(target=self.carregar_dados)
        inicia.start()


    def carregaricones(self):

        self.calendarioicon = PhotoImage(file='icones\\calendario.png',master=self.master)
        self.setadireitaicon = PhotoImage(file='icones\\seta direita.png',master=self.master)
        self.setaesquerdaicon = PhotoImage(file='icones\\seta esquerda.png',master=self.master)
        self.image_fechar=PhotoImage(file='icones\\fechar_button.png',master=self.master)

        self.imagemotor1 ='icones\\fundo motores 1.png'
        self.imagemotor2 ='icones\\fundo motores 2.png'
        self.imagemotoresgeral ='icones\\fundo motores geral.png'
        self.image_copyright ='icones\\copyright.png'
        self.image_equilibrio='icones\\equilibrio de carga.png'
        self.image_calendario_motores='icones\\data e hora.png'
        self.image_fundo_azul='icones\\fundo azul.png'
        self.image_data_inicio='icones\\data e hora inicial.png'
        self.image_data_final='icones\\data e hora final.png'
        self.image_percurso_info='icones\\percurso info.png'
        self.image_calendario_geral='icones\\calendario_opcoes.png'

        
    def abre_dados_tratados(self):
        print("CIU")
        self.dadoscarregados=False
        self.carregar_tela_threading()
            
        try:
            
            self.df_dadosnovos=pd.read_json('Dados.json')
            #print("Leu")
        except:
            try:
                self.df_dadosnovos=pd.read_excel('Dados.xlsx')
                self.df_dadosnovos.to_json('Dados.json',index=False)
                #print("Abriu excel pq n tinha json. Salvando em .json para futuro")
                messagebox.showinfo("Atenção", "Não existem dados tratados atualizados. Dados anteriores foram abertos com sucesso e foram atualizados")
                self.dadoscarregados=True

            except:
                messagebox.showerror("Erro", "Não existem dados tratados")
                self.dadoscarregados=True

        t_linhas_i=len(self.df_dadosnovos)
        

        t_linhas_f=len(self.df_dadosnovos)
        if t_linhas_f !=t_linhas_i:
            self.df_dadosnovos.to_json('Dados.json',index=False)
        dados=self.df_dadosnovos
        titulos=dados.columns
        self.titulos_number=[]
        filtro=dados[dados['PERCURSO']==14]#percurso 14 pra diminuir o processamento 
        for titulo in titulos:
            try:
                valor=f"MÉDIA ({titulo}) = {filtro[titulo]*10}"
                self.titulos_number.append(titulo)
            except:
                pass

        #print(self.titulos_number)
        self.intervalo_tendencia = self.df_dadosnovos

        percursos_lista=self.df_dadosnovos['PERCURSO'].to_list()
        percursos_fixos=['TODOS']
        current_rep=0
        contagem_rep=1
        for valor in percursos_lista:
                if not valor in percursos_fixos:
                    if valor == current_rep:
                        contagem_rep+=1
                    else:
                        current_rep=valor
                        contagem_rep=1

                    if contagem_rep>20:
                        percursos_fixos.append(valor)
                        #print(valor)

        self.percursos_lista=percursos_fixos
        self.percursos_lista[1:]=sorted(self.percursos_lista[1:])
        self.datas_list=list(set(self.df_dadosnovos['DATA E HORA'].str.slice(stop=-6).to_list()))
        lista_perc=self.df_dadosnovos['PERCURSO'].to_list()
        inicios=[]
        finais=[]
        self.points=[]
        for item in lista_perc:
            item=item.split("--")
            try:
                inicios.append(int(item[0]))
                finais.append(int(item[1]))
                self.points.append(item)
            except:
                pass
        inicios=list(set(inicios))
        finais=list(set(finais))
        self.inicio_tendencia2.config(values=inicios)
        self.fim_tendencia2.config(values=finais)
        self.dadoscarregados=True



    def telacarregando(self,label):
        frames=[]
        for z in range(0,22):
            img=PhotoImage(file=f'icones\\carregamento_frames\\frame_{z}.png',master=self.master)
            frames.append(img)

        while not self.dadoscarregados:
                for i in range(0,22):
                    label.config(image=frames[i])
                    time.sleep(0.02)

    def dataselected(self,master,label):
            self.calendario_ativado=False
            self.finalx=0
            self.finaly=50
            def start_move(event):
                # Iniciar movimento
                self.startx = topmaster.winfo_pointerx()
                self.starty = topmaster.winfo_pointery()

            def stop_move(event):
                # Parar movimento
                try:
                    self.finalx = self.current_x_drag
                    self.finaly = self.current_y_drag
                except:
                    self.current_x_drag=0
                    self.current_y_drag=0


            def on_drag(event):
                # Atualizar posição da janela
                #print(event.x,event.y)
                deltax =  topmaster.winfo_pointerx()-(self.startx-self.finalx)
                deltay = topmaster.winfo_pointery()-(self.starty-self.finaly)
                x = deltax
                y =  deltay
                self.current_x_drag=x
                self.current_y_drag=y
                topmaster.geometry(f"+{x}+{y}")


            if self.calendario_ativado:
                return 
            self.calendario_ativado=True
            atual=label.cget("text")
            #print(atual)
            if atual !="NÃO SELECIONADA":
                month=int(atual.split("/")[0])
                day=int(atual.split("/")[1])
                year=int(atual.split("/")[2].split(" ")[0])
                hora=atual.split("/")[2].split(" ")[1].split(":")[0]
                min=atual.split("/")[2].split(" ")[1].split(":")[1]
            else:
                data1=self.datas_list[0].split("/")
                #print(data1)
                day=int(data1[1])
                month=int(data1[0])
                year=int(data1[2])
                hora=00
                min=00
       
            topmaster = tk.Toplevel(master,background='pink')
            topmaster.attributes('-topmost',True)
            topmaster.overrideredirect(True)
            topmaster.wm_attributes("-transparentcolor", 'pink')
            topmaster.geometry("600x780+0+50")
            topmaster.title("Selecione a data")




            top=tk.Frame(topmaster,background='pink',width=550,height=780)
            top.place(x=10,y=10)

            topmaster.bind("<ButtonPress-1>", start_move)
            topmaster.bind("<ButtonRelease-1>",stop_move)
            topmaster.bind("<B1-Motion>", on_drag)

            self.colocarfundo(top,self.image_calendario_geral,100,100,bd='pink')
            calendar = Calendar(top,
                                selectmode='day',
                                year=year, 
                                month=month, 
                                day=day,
                                showweeknumbers=False,
                                showothermonthdays=False,
                                normalbackground='red',
                                weekendbackground='red',
                                headersbackground=self.rgb_to_color((70,177,225)),
                                background=self.rgb_to_color((70,177,225)),
                                foreground='black',
                                bordercolor='black',
                                font=('Arial', 16)
                                )

            for data in self.datas_list:
                data=data.split('/')
                #print(data)
                dd=int(data[1])
                mm=int(data[0])
                yy=int(data[2])
                day = datetime.date(yy, mm, dd)
                calendar.calevent_create(day, "", tags="hi")
                calendar.tag_config("hi", background="green")
 

            # Caixas de seleção de hora, minuto e segundo
            timeframe=tk.Frame(top,background=self.rgb_to_color((70,177,225)))
            timeframe.place(x=217,y=385)
            calendar.place(x=80, y=90)
            hora_label = ttk.Label(timeframe, text="Hr  -  Min",font=('Arial',12),background=self.rgb_to_color((70,177,225)))
            hora_label.pack()
            frame_time=tk.Frame(timeframe,background=self.rgb_to_color((70,177,225)))
            frame_time.pack()
            hora_spinbox = tk.Spinbox(frame_time, from_=0, to=23, width=3,font=('Arial', 16),textvariable=tk.StringVar(value=hora),background=self.rgb_to_color((70,177,225)),foreground='black')
            minuto_spinbox = tk.Spinbox(frame_time, from_=0, to=59,font=('Arial', 16) ,increment=5, width=3,textvariable=tk.StringVar(self.master,value=min),background=self.rgb_to_color((70,177,225)),foreground='black')
            minuto_spinbox.pack(side='right')
            hora_spinbox.pack(side='right')
            

            def pegar_data_hora():
                data = calendar.get_date().split("/")
                i=0
                for tempo in data:
                    if len(tempo)==1:
                        data[i]="0"+tempo
                    i+=1
                data[2]="20"+data[2]
                data_formatada = "/".join([data[0], data[1], data[2]])

                hora = hora_spinbox.get()
                minuto = minuto_spinbox.get()


                hora_formatada = f"{hora.zfill(2)}:{minuto.zfill(2)}"

                data_hora_formatada = f"{data_formatada} {hora_formatada}"
                texto=data_hora_formatada
                #print(texto)
            
                if texto[:-6] in self.datas_list:
                    if not texto in self.df_dadosnovos['DATA E HORA'].values:
                        self.calendario_ativado=False
                        label.config(text=texto)
                        topmaster.destroy()
                        messagebox.showinfo(title="Data inválida",message= "Horário para esta data não esta no banco de dados")
                        return 
                else:
                    self.calendario_ativado=False
                    label.config(text=texto)
                    topmaster.destroy()
                    messagebox.showinfo(title="Data inválida",message= "Data não está no banco de dados")
                    return 


                label.config(text=texto)
                topmaster.destroy()
                if master==self.tbAnaliseMotores:
                    self.todos_graficos_motores()
                elif master==self.tbTendenciaConsumo:
                    if self.caixadata_hora_tendencia_consumo_inicio.cget("text")!="NÃO SELECIONADA":
                        if self.caixadata_hora_tendencia_consumo_final.cget("text")!="NÃO SELECIONADA":
                            self.todastendenciasativas()
                self.calendario_ativado=False

            btn_selecionar = ttk.Button(timeframe, text="Selecionar", command=pegar_data_hora)
            btn_selecionar.pack(side='bottom')
            def fechar_janela():
                self.calendario_ativado=False
                topmaster.destroy()
                return

            closebutton=Button(topmaster,command=fechar_janela,image=self.image_fechar,borderwidth=0,border=0,highlightthickness=0)
            closebutton.place(x=430,y=35)
            topmaster.protocol("WM_DELETE_WINDOW", fechar_janela)

    def rgb_to_color(self,rgblist):

        new='#{:02x}{:02x}{:02x}'.format(rgblist[0],rgblist[1],rgblist[2])
        return new

    def scroll_x_graficoz(self,event=None):
        x=self.intervalo_tendencia["DATA E HORA"]
        x_lista = list(x)
        tot=len(x_lista)
        cx=float(self.scalex_scrollbutton.get())
        self.escala_x_grafico=cx
        if not len(x_lista)>350:
            n = int(((cx/100)) *len(x_lista))
            step=int(len(x_lista)/n)
        else:
            step = int((1-(cx/100)) *len(x_lista))+1

        ax=plt.gca()
        xz,yz=ax.get_xlim(),ax.get_ylim()
        plt.xticks(range(0, len(x_lista), step), [x_lista[i] for i in range(0, len(x_lista), step)], rotation=0)

        plt.gca().set_xlim(xz)
        plt.gca().set_ylim(yz)
        plt.draw()


    def func_percurso(self,event):
       
            self.titulos_number #todos os titulos ou cabeçalhos 
            valor_caixa=""
            inicio=self.inicio_tendencia2.get()
            fim=self.fim_tendencia2.get()
            titulo=self.bombox_percurso_titulo.get()
            new_finals=[]
            if inicio != "":
                for point in self.points:
                    if point[0]==inicio:
                        if not point[1] in new_finals:
                            new_finals.append(point[1])

                self.fim_tendencia2.config(values=new_finals)

            new_iniciais=[]
            cond=False
            if fim != "":
                for point in self.points:
                    if point[0]==inicio:
                        if point[1] == fim:
                            cond=True
                if not cond:
                    for point in self.points:
                        if point[0]==inicio:
                            if point[1] != fim:  
                                self.fim_tendencia2.set(point[0])


            inicio=self.inicio_tendencia2.get()
            fim=self.fim_tendencia2.get()
            titulo=self.bombox_percurso_titulo.get()

            if inicio == "" or fim =="" or titulo=="":
                return 

            i=0
            indice=0
            for tit in self.titulos_capa:
   
                if titulo==tit:
                    indice=i
    
                i+=1

            titulo=self.titulos_number_select[indice]
            try:
                inicio=int(inicio)
            except:
                inicio=0
            try:
                fim=int(fim)
            except:
                fim=0
            inicio=int(inicio)
            fim=int(fim)
            filtro=self.df_dadosnovos[self.df_dadosnovos['PERCURSO']==f'{inicio}--{fim}']
            print(filtro)
            valor1=f"Mínimo ({titulo[0:5]}) = {round(filtro[titulo].min(),3)}"
            valor2=f"Média ({titulo[0:5]}) = {round(filtro[titulo].mean(),3)}"
            valor3=f"Máximo ({titulo[0:5]}) = {round(filtro[titulo].max(),3)}"
            valor_caixa+=f" {valor1} \n {valor2} \n {valor3}"


            self.label_text_info.config(text=valor_caixa,justify="left")

    def percursos(self):

        plt,ax1,fig,canvas,toolbar=criagrafico(master=self.frame_grafico_perc).geragrafico()
        plt.scatter(-43.1,-22.8,marker='o', color='pink', label='Baía de Guanabara')
        plt.tight_layout()
        plt.axis("equal")
        self.atualfig=fig
        self.atualtoolbar=toolbar
        percurso(fig,ax1,canvas,self.tbPercursos,interface=True)

    

    def analise_motor1(self): #Definição da função atrelada ao botão de diagnóstico do motor 1

        if self.atualiza_variaveis_motores():
            if self.E1_ROTACAO_RPM <= 800:
                self.consumo_ideal_gkwh_E1 = -(9*(10**(-5))*(self.E1_ROTACAO_RPM**2))+(0.0335*self.E1_ROTACAO_RPM)+220.24
            else:
                self.consumo_ideal_gkwh_E1 = (0.0023*(self.E1_ROTACAO_RPM**2))-(3.8039*self.E1_ROTACAO_RPM)+1755.2
            
            self.E1_CONSUMO_GKWH = self.E1_CONSUMO_GH/self.E1_POTENCIA_KW

            # Definição da equação que rege o comportamento da potência ideal baseado nas curvas de desempenho dos testes de bancada
            self.potencia_ideal_kw_E1 = (0.0055*(self.E1_ROTACAO_RPM**2))-(3.1582*self.E1_ROTACAO_RPM)+738.99

            # Definição dos condicionais que farão a comparação entre consumo real e ideal e plotagem do diagnóstico na interface
            if 0.97*self.potencia_ideal_kw_E1 <= self.E1_POTENCIA_KW <= 1.03*self.potencia_ideal_kw_E1:
                consumo_info_text= "Consumo adequado"
                if self.potencia_ideal_kw_E1 != self.E1_POTENCIA_KW:
                    analise1 = " Nesta RPM (" + str(round(self.E1_ROTACAO_RPM,2)) + " rpm), o motor deveria estar fornecendo " + str(round(self.potencia_ideal_kw_E1,2)) + " kW de potência, com um consumo específico de " + str(round(self.consumo_ideal_gkwh_E1,2)) + " g/kwh.\n O Motor 1 está fornecendo " + str(round(self.E1_POTENCIA_KW,2)) + " kW de potência com um consumo específico de " + str(round(self.E1_CONSUMO_GKWH,2)) + " g/kwh. \n Esta diferença de potência e de consumo indica que este motor está operando de forma satisfatória."
                else:
                    analise1 = "O motor 1 está fornecendo " + str(round(self.E1_POTENCIA_KW,2)) + " kW de potência com um consumo específico de " + str(round(self.E1_CONSUMO_GKWH,2)) + " g/kwh. \n Nesta RPM (" + str(round(self.E1_ROTACAO_RPM,2)) + " rpm), o motor está atuando nas condições ideais de operação."
            
            elif 1.03*self.potencia_ideal_kw_E1 < self.E1_POTENCIA_KW:
                consumo_info_text = "CONSUMO ACIMA DO IDEAL"
                analise1 = " Nesta RPM (" + str(round(self.E1_ROTACAO_RPM,2)) + " rpm), o motor deveria estar fornecendo " + str(round(self.potencia_ideal_kw_E1,2)) + " kW de potência, com um consumo específico de " + str(round(self.consumo_ideal_gkwh_E1,2)) + " g/kwh.\n O Motor 1 está fornecendo " + str(round(self.E1_POTENCIA_KW,2)) + " kW de potência com um consumo específico de " + str(round(self.E1_CONSUMO_GKWH,2)) + " g/kwh.\n Esta diferença de potência e de consumo indica que este motor não está operando de forma satisfatória.\n Redução de potência pode ser causada por:\n - Fornecimento insuficiente de combustível (vazamento/restrição)\n - Combustível incorreto ou contaminado\n - Sincronização incorreta de injeção\n - Restrição na admissão de ar\n - Perda de pressão no turbo carregador\n - Falha no sistema de alta pressão de combustível\n - Perda de compressão no motor."
        
            elif 0.97*self.potencia_ideal_kw_E1 > self.E1_POTENCIA_KW:
                if self.E1_CONSUMO_GKWH <= 0:
                    consumo_info_text = "MOTOR DESLIGADO"
                    analise1 = " O motor 1 está desligado."
                else:
                    consumo_info_text = "CONSUMO ABAIXO DO IDEAL"
                    analise1 = " Nesta RPM (" + str(round(self.E1_ROTACAO_RPM,2)) + " rpm), o motor deveria estar fornecendo " + str(round(self.potencia_ideal_kw_E1,2)) + " kW de potência, com um consumo específico de " + str(round(self.consumo_ideal_gkwh_E1,2)) + " g/kwh.\n O Motor 1 está fornecendo " + str(round(self.E1_POTENCIA_KW,2)) + " kW de potência com um consumo específico de " + str(round(self.E1_CONSUMO_GKWH,2)) + " g/kwh. \n Esta diferença de potência e de consumo indica que este motor não está operando de forma satisfatória.\n Redução de potência pode ser causada por:\n - Fornecimento insuficiente de combustível (vazamento/restrição)\n - Combustível incorreto ou contaminado\n - Sincronização incorreta de injeção\n - Restrição na admissão de ar\n - Perda de pressão no turbo carregador\n - Falha no sistema de alta pressão de combustível\n - Perda de compressão no motor."
            
            #Plotando potência, rotação e consumo na interface
            if self.E1_CONSUMO_GKWH <= 0:
                pontenciatext=""
                rotacaotext=""
                consumotext=""
            else:
                pontenciatext="Potência: " + str(round(self.E1_POTENCIA_KW,2)) + "kW"
                rotacaotext="Rotação: " + str(round(self.E1_ROTACAO_RPM,2)) + "rpm"
                consumotext="Consumo: " + str(round(self.E1_CONSUMO_GKWH,2)) + "g/kWh"

            if self.E1_DIRECAO ==0:
                direcao_text="Rumo: Parado"
            elif self.E1_DIRECAO ==2:
                direcao_text="Rumo: Plataforma"
            elif self.E1_DIRECAO ==1:
                direcao_text="Rumo: Porto"

            # Plotando o número do percurso na interface
            trajetoria_text="Trajetória: Percurso " + str(self.E1_PERCURSO)
            trajetoriaMotor1 = 'Em viagem no percurso '+ str(self.E1_PERCURSO)
            altura_onda_text = "Altura de onda: " + str(round(self.SIG_WAVE_HEIGHT_M,3))
            velocida_vento_text = "Vel vento: " + str(round(self.WIND_SPEED_M_PER_S,3)) + " m/s"
            velocida_servico_text = "Vel serviço: " + str(round(self.VESSEL_KNOTS,3)) + " nós"


            # Definição dos valores de rotação, potência e consumo para montar as curvas ideais conforme os testes de bancada
            x = [449,600,721,798,901]
            y = [427,829,1246,1782,2321]
            z = [217.4,209.5,197.7,191.6,196.5]
            
            textolabel=f'''
{consumo_info_text}

{pontenciatext}
{rotacaotext}
{consumotext}
'''
            textolabel_geral=f'''
{trajetoria_text}
{direcao_text}
{altura_onda_text}
{velocida_vento_text}
{velocida_servico_text}
'''
            self.label_info_geral.config(text=textolabel_geral)
            self.label_info_motor1.config(text=textolabel)
            plt,ax1,fig,canvas,toolbar=criagrafico(master=self.frame_grafico_motor1).geragrafico()
            self.figatual=len(plt.get_fignums())
            ax1.set_xlabel('Rotação (RPM)',fontsize=8)
            ax1.plot(x,z, color = 'g')
            ax1.set_ylabel('Consumo (g/kWh)', color = 'g')
            ax1.plot(x,z, color = 'g')
            ax1.tick_params(axis='y', labelcolor = 'g')
            plt.plot(self.E1_ROTACAO_RPM,self.E1_CONSUMO_GKWH,'s',color='green')
            plt.title(f'Consumo / Potência x Rotação - Motor 1   {self.caixadatamotores.cget("text")}')
            plt.ylim(150,250)
        
            ax2 = ax1.twinx()
            ax2.set_ylabel('Potência (kW)', color = 'r') 
            ax2.plot(x,y, color = 'r')
            ax2.tick_params(axis='y', labelcolor = 'r')
            plt.plot(self.E1_ROTACAO_RPM,self.E1_POTENCIA_KW,'s',color='red')
            self.atualfig=fig
            self.atualtoolbar=toolbar
            self.relatorio_mot_1=(f''' 
Motor 1

Potência:{str(round(self.E1_POTENCIA_KW,2))}kW
Rotação: {str(round(self.E1_ROTACAO_RPM,2))} rpm
Consumo: {str(round(self.E1_CONSUMO_GKWH,2))} g/kWh

Análise
{analise1}''')
            

            self.relatorio_mot_geral=f'''
--------INFORMAÇÕES GERAIS--------
RELATÓRIO GERADO EM {self.data_escrita()[0]}.
Data e hora informadas: {self.data1}
{trajetoria_text}
{trajetoriaMotor1}
{altura_onda_text}
{velocida_vento_text }
{velocida_servico_text}

'''
            
    def data_escrita(self):
        
        a=str(dt.today())
        meses=["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]

        #print(a[:-7])
        a=a[:-7]

        horario=a[-8:]
        ano = a[:4]
        mes=a[5:7]
        dia=a[8:10]
        data_escrita=f"{dia} de {meses[int(mes)-1]} de {ano}. {horario}"
        return data_escrita,a

    def extraigrafico(self):
        fig=self.atualfig        
        self.figsmotores.append(fig)
        figs_existentes = set(plt.get_fignums())
        figs_lista = set([fig.number for fig in self.figsmotores])
        for fig_num in figs_existentes:
            fig = plt.figure(fig_num)
            if fig not in self.figsmotores:
                plt.close(fig)
                #print(f"Deletou {fig}")

        plt.show()

    def atualiza_variaveis_motores(self):
        self.linha_motor=self.linha_motor
        self.numero_de_linhas = self.linha_motor.shape[0]
        if self.numero_de_linhas >= 1:
            for i in self.linha_motor.index: #precisa fazer assim pq o indice é original do data origem (nao é 0)
                self.E1_PERCURSO = self.linha_motor.at[i,"PERCURSO"]
                self.E1_DIRECAO = self.linha_motor.at[i,"ROTA"]
                self.E1_CONSUMO_GH = self.linha_motor.at[i,"E1_CONSUMO_GH"]
                self.E1_POTENCIA_KW = self.linha_motor.at[i,"E1_POTÊNCIA_KW"]
                self.E1_ROTACAO_RPM = self.linha_motor.at[i,"E1_ROTAÇÃO_RPM"]
                self.SIG_WAVE_HEIGHT_M = self.linha_motor.at[i,"SIG_WAVE_HEIGHT_M"]
                self.WIND_SPEED_M_PER_S = self.linha_motor.at[i,"WIND_SPEED_M_PER_S"]
                self.VESSEL_KNOTS = self.linha_motor.at[i,"VESSEL_KNOTS"]
                self.direcao_navio=self.linha_motor.at[i,"DIREÇÃO NAVIO"]
                self.rota=self.linha_motor.at[i,"ROTA"]
                self.lat_navio=self.linha_motor.at[i,"LAT"]
                self.lon_navio=self.linha_motor.at[i,"LON"]
                self.E2_PERCURSO = self.linha_motor.at[i,"PERCURSO"]
                self.E2_DIRECAO = self.linha_motor.at[i,"ROTA"]
                self.E2_CONSUMO_GH = self.linha_motor.at[i,"E2_CONSUMO_GH"]
                self.E2_POTENCIA_KW = self.linha_motor.at[i,"E2_POTÊNCIA_KW"]
                self.E2_ROTACAO_RPM = self.linha_motor.at[i,"E2_ROTAÇÃO_RPM"]
                self.SIG_WAVE_HEIGHT_M = self.linha_motor.at[i,"SIG_WAVE_HEIGHT_M"]
                self.WIND_SPEED_M_PER_S = self.linha_motor.at[i,"WIND_SPEED_M_PER_S"]
                self.VESSEL_KNOTS = self.linha_motor.at[i,"VESSEL_KNOTS"]
                self.carga_E1 = self.E1_POTENCIA_KW/2321
                self.str_carga_E1 = str(round(self.carga_E1*100,2)) + "%"
                self.carga_E2 = self.E2_POTENCIA_KW/2317
                self.str_carga_E2 = str(round(self.carga_E2*100,2)) + "%"
                self.E1_CONSUMO_GKWH = self.E1_CONSUMO_GH/self.E1_POTENCIA_KW
                self.E2_CONSUMO_GKWH = self.E2_CONSUMO_GH/self.E2_POTENCIA_KW



            return True
        
        else:
            return False

    #Definição da função atrelada ao botão de diagnóstico do motor 2
    def analise_motor2(self): #Definição da função atrelada ao botão de diagnóstico do motor 1
        if self.atualiza_variaveis_motores():
            if self.E2_ROTACAO_RPM <= 800:
                self.consumo_ideal_gkwh_E2 = -(9*(10**(-5))*(self.E2_ROTACAO_RPM**2))+(0.0335*self.E2_ROTACAO_RPM)+220.24
            else:
                self.consumo_ideal_gkwh_E2 = (0.0023*(self.E2_ROTACAO_RPM**2))-(3.8039*self.E2_ROTACAO_RPM)+1755.2
            
            self.E2_CONSUMO_GKWH = self.E2_CONSUMO_GH/self.E2_POTENCIA_KW

            # Definição da equação que rege o comportamento da potência ideal baseado nas curvas de desempenho dos testes de bancada
            self.potencia_ideal_kw_E2 = (0.0055*(self.E2_ROTACAO_RPM**2))-(3.1582*self.E2_ROTACAO_RPM)+738.99

            # Definição dos condicionais que farão a comparação entre consumo real e ideal e plotagem do diagnóstico na interface
            if 0.97*self.potencia_ideal_kw_E2 <= self.E2_POTENCIA_KW <= 1.03*self.potencia_ideal_kw_E2:
                consumo_info_text= "Consumo adequado"
                if self.potencia_ideal_kw_E2 != self.E2_POTENCIA_KW:
                    analisE2 = " Nesta RPM (" + str(round(self.E2_ROTACAO_RPM,2)) + " rpm), o motor deveria estar fornecendo " + str(round(self.potencia_ideal_kw_E2,2)) + " kW de potência, com um consumo específico de " + str(round(self.consumo_ideal_gkwh_E2,2)) + " g/kwh.\n O Motor 1 está fornecendo " + str(round(self.E2_POTENCIA_KW,2)) + " kW de potência com um consumo específico de " + str(round(self.E2_CONSUMO_GKWH,2)) + " g/kwh. \n Esta diferença de potência e de consumo indica que este motor está operando de forma satisfatória."
                else:
                    analisE2 = "O motor 2 está fornecendo " + str(round(self.E2_POTENCIA_KW,2)) + " kW de potência com um consumo específico de " + str(round(self.E2_CONSUMO_GKWH,2)) + " g/kwh. \n Nesta RPM (" + str(round(self.E2_ROTACAO_RPM,2)) + " rpm), o motor está atuando nas condições ideais de operação."
            
            elif 1.03*self.potencia_ideal_kw_E2 < self.E2_POTENCIA_KW:
                consumo_info_text = "CONSUMO ACIMA DO IDEAL"
                analisE2 = " Nesta RPM (" + str(round(self.E2_ROTACAO_RPM,2)) + " rpm), o motor deveria estar fornecendo " + str(round(self.potencia_ideal_kw_E2,2)) + " kW de potência, com um consumo específico de " + str(round(self.consumo_ideal_gkwh_E2,2)) + " g/kwh.\n O Motor 1 está fornecendo " + str(round(self.E2_POTENCIA_KW,2)) + " kW de potência com um consumo específico de " + str(round(self.E2_CONSUMO_GKWH,2)) + " g/kwh.\n Esta diferença de potência e de consumo indica que este motor não está operando de forma satisfatória.\n Redução de potência pode ser causada por:\n - Fornecimento insuficiente de combustível (vazamento/restrição)\n - Combustível incorreto ou contaminado\n - Sincronização incorreta de injeção\n - Restrição na admissão de ar\n - Perda de pressão no turbo carregador\n - Falha no sistema de alta pressão de combustível\n - Perda de compressão no motor."
        
            elif 0.97*self.potencia_ideal_kw_E2 > self.E2_POTENCIA_KW:
                if self.E2_CONSUMO_GKWH <= 0:
                    consumo_info_text = "MOTOR DESLIGADO"
                    analisE2 = " O motor 2 está desligado."
                else:
                    consumo_info_text = "CONSUMO ABAIXO DO IDEAL"
                    analisE2 = " Nesta RPM (" + str(round(self.E2_ROTACAO_RPM,2)) + " rpm), o motor deveria estar fornecendo " + str(round(self.potencia_ideal_kw_E2,2)) + " kW de potência, com um consumo específico de " + str(round(self.consumo_ideal_gkwh_E2,2)) + " g/kwh.\n O Motor 1 está fornecendo " + str(round(self.E2_POTENCIA_KW,2)) + " kW de potência com um consumo específico de " + str(round(self.E2_CONSUMO_GKWH,2)) + " g/kwh. \n Esta diferença de potência e de consumo indica que este motor não está operando de forma satisfatória.\n Redução de potência pode ser causada por:\n - Fornecimento insuficiente de combustível (vazamento/restrição)\n - Combustível incorreto ou contaminado\n - Sincronização incorreta de injeção\n - Restrição na admissão de ar\n - Perda de pressão no turbo carregador\n - Falha no sistema de alta pressão de combustível\n - Perda de compressão no motor."
            
            #Plotando potência, rotação e consumo na interface
            if self.E2_CONSUMO_GKWH <= 0:
                pontenciatext=""
                rotacaotext=""
                consumotext=""
            else:
                pontenciatext="Potência: " + str(round(self.E2_POTENCIA_KW,2)) + "kW"
                rotacaotext="Rotação: " + str(round(self.E2_ROTACAO_RPM,2)) + "rpm"
                consumotext="Consumo: " + str(round(self.E2_CONSUMO_GKWH,2)) + "g/kWh"

            if self.E2_DIRECAO ==0:
                direcao_text="Parado"
            elif self.E2_DIRECAO ==2:
                direcao_text="Rumo à plataforma"
            elif self.E2_DIRECAO ==1:
                direcao_text="Rumo ao porto"

            # Plotando o número do percurso na interface
            trajetoria_text="Trajetória: Percurso " + str(self.E2_PERCURSO)
            trajetoriaMotor1 = f"Em viagem no percurso' {str(self.E2_PERCURSO)}"
            altura_onda_text = "Altura de onda: " + str(self.SIG_WAVE_HEIGHT_M)
            velocida_vento_text = "Vel do vento: " + str(self.WIND_SPEED_M_PER_S) + " m/s"
            velocida_servico_text = "Vel de serviço: " + str(self.VESSEL_KNOTS) + " nós"


            # Definição dos valores de rotação, potência e consumo para montar as curvas ideais conforme os testes de bancada
            x = [449,600,721,798,901]
            y = [427,829,1246,1782,2321]
            z = [217.4,209.5,197.7,191.6,196.5]
            
            textolabel=f'''
{consumo_info_text}

{pontenciatext}
{rotacaotext}
{consumotext}
'''

            self.label_info_motor2.config(text=textolabel)
            plt,ax1,fig,canvas,toolbar=criagrafico(master=self.frame_grafico_motor1).geragrafico()
            self.figatual=len(plt.get_fignums())
            ax1.set_xlabel('Rotação (RPM)',fontsize=8)
            ax1.plot(x,z, color = 'g')
            ax1.set_ylabel('Consumo (g/kWh)', color = 'g')
            ax1.plot(x,z, color = 'g')
            ax1.tick_params(axis='y', labelcolor = 'g')
            plt.plot(self.E2_ROTACAO_RPM,self.E2_CONSUMO_GKWH,'s',color='green')
            plt.title(f'Consumo / Potência x Rotação - Motor 2   {self.caixadatamotores.cget("text")}')
            plt.ylim(150,250)
        
            ax2 = ax1.twinx()
            ax2.set_ylabel('Potência (kW)', color = 'r') 
            ax2.plot(x,y, color = 'r')
            ax2.tick_params(axis='y', labelcolor = 'r')
            plt.plot(self.E2_ROTACAO_RPM,self.E2_POTENCIA_KW,'s',color='red')
            self.atualfig=fig
            self.atualtoolbar=toolbar
            self.relatorio_mot_2=f'''
Motor 2

Potência:{str(round(self.E2_POTENCIA_KW,2))}kW
Rotação: {str(round(self.E2_ROTACAO_RPM,2))} rpm
Consumo: {str(round(self.E2_CONSUMO_GKWH,2))} g/kWh

Análise
{analisE2}'''
            
    # Definição da funçãon que realizará a análise de equilíbrio de carga entre os motores 1 e 2
    def equilibrio_carga(self):
        if self.atualiza_variaveis_motores():
            if self.E1_ROTACAO_RPM <= 800:
                self.consumo_ideal_gkwh_E1 = -(9*(10**(-5))*(self.E1_ROTACAO_RPM**2))+(0.0335*self.E1_ROTACAO_RPM)+220.24
            else:
                self.consumo_ideal_gkwh_E1 = (0.0023*(self.E1_ROTACAO_RPM**2))-(3.8039*self.E1_ROTACAO_RPM)+1755.2

            if self.E2_ROTACAO_RPM <= 800:
                self.consumo_ideal_gkwh_E2 = -(9*(10**(-5))*(self.E2_ROTACAO_RPM**2))+(0.0335*self.E2_ROTACAO_RPM)+220.24
            else:
                self.consumo_ideal_gkwh_E2 = (0.0023*(self.E2_ROTACAO_RPM**2))-(3.8039*self.E2_ROTACAO_RPM)+1755.2

            if self.E1_CONSUMO_GKWH <= 0:
                analise_equilibrio = " Os motores estão desligados."
            else:             
                if abs((self.E1_ROTACAO_RPM-self.E2_ROTACAO_RPM)/self.E1_ROTACAO_RPM) <= 0.05:
                    if abs((self.E1_POTENCIA_KW-self.E2_POTENCIA_KW)/self.E1_POTENCIA_KW) <= 0.05:
                        analise_equilibrio = " Os motores estão em equilíbrio de rotação e em equilíbrio de carga."
                    else:
                        analise_equilibrio = " Os motores estão em equilíbrio de rotação, porém em desequilíbrio de carga.\n O motor 1 está fornecendo " + self.str_carga_E1 + " de carga, enquanto o motor 2 está fornecendo " + self.str_carga_E2 + " de carga.\n Este desequilíbrio afeta a economia de combustível, bem como o desempenho do navio.\n Motores de um mesmo sistema propulsivo com cargas diferentes conduzem a uma condição onde um deles é mais exigido que o outro,\n acarretando aumento de consumo e contribuindo para aumentar o desgaste de seus componentes mecânicos,\n gerando falhas e comprometendo a segurança do navio."
                else:
                    analise_equilibrio = " Os motores estão em desequilíbrio de rotação.\n O motor 1 está com uma rotação de " + str(round(self.E1_ROTACAO_RPM,2)) + " rpm, enquanto o motor 2 está com uma rotação de " + str(round(self.E2_ROTACAO_RPM,2)) + " rpm.\n Este desequilíbrio afeta a economia de combustível, bem como o desempenho do navio.\n Motores de um mesmo sistema propulsivo com cargas diferentes conduzem a uma condição onde um deles é mais exigido que o outro,\n acarretando aumento de consumo e contribuindo para aumentar o desgaste de seus componentes mecânicos,\n gerando falhas e comprometendo a segurança do navio."

            # Definição dos valores de consumo e rotação equilibrados
            self.CONSUMO_EQUILIBRADO_GH = (self.E1_CONSUMO_GH+self.E2_CONSUMO_GH)/2
            self.CONSUMO_EQUILIBRADO_GKWH = (self.E1_CONSUMO_GKWH+self.E2_CONSUMO_GKWH)/2
            self.POTENCIA_EQUILIBRADA = ((-9)*(10**(-10))*((self.CONSUMO_EQUILIBRADO_GH)**2))+(0.0058*(self.CONSUMO_EQUILIBRADO_GH))-119.5
            self.ROTACAO_EQUILIBRADA = ((-2)*(10**(-9))*((self.CONSUMO_EQUILIBRADO_GH)**2))+(0.0024*(self.CONSUMO_EQUILIBRADO_GH))+251.69
            
            potenciatotal= ((-9)*(10**(-10))*((2*self.CONSUMO_EQUILIBRADO_GH)**2))+(0.0058*(2*self.CONSUMO_EQUILIBRADO_GH))-119.5
            consumototal=self.CONSUMO_EQUILIBRADO_GKWH*2

            #Plotando potência, rotação e consumo equilibrados na interface
            if self.E1_CONSUMO_GKWH <= 0:
                potencia_text_equilibrada =  "Motor Desligado                              "
                rotacao_text_equilibrada =""
                consumo_text_equilibrada =""
                consumo_text_total=""
                potencia_text_total=""
            else:
                potencia_text_equilibrada =   "Potência: " + str(round(self.POTENCIA_EQUILIBRADA,2))+ " kW"
                rotacao_text_equilibrada ="Rotação: " + str(round(self.ROTACAO_EQUILIBRADA,2)) + " rpm"
                consumo_text_equilibrada ="Consumo: " + str(round(self.CONSUMO_EQUILIBRADO_GKWH,2)) + " g/kWh"
                consumo_text_total=f"Consumo: {round(consumototal,3)} g/kWh"
                potencia_text_total=f"Potência: {round(potenciatotal,3)} kW"

            textolabel=f'''
   {potencia_text_equilibrada}                               {consumo_text_total}
   {rotacao_text_equilibrada}                                {potencia_text_total}
{consumo_text_equilibrada}                                                              '
'''
            self.label_info_equilibrio.config(text=textolabel)

            x = [449, 600, 721, 798, 901]
            y = [427, 829, 1246, 1782, 2321]
            z = [217.4, 209.5, 197.7, 191.6, 196.5]

            plt,ax1,fig,canvas,toolbar=criagrafico(master=self.frame_grafico_motor1).geragrafico()
            # Plotagem das curvas ideais e dos pontos de operação reais
            ax1.set_xlabel('Rotação (RPM)',fontsize=8)
            ax1.plot(x, z, color='g', label='Curva de Consumo Ideal')
            ax1.set_ylabel('Consumo (g/kWh)', color='g')
            ax1.tick_params(axis='y', labelcolor='g')

            ax1.scatter(self.E1_ROTACAO_RPM, self.E1_CONSUMO_GKWH, marker='s', color='green', label='Consumo Motor 1')
            ax1.scatter(self.E2_ROTACAO_RPM, self.E2_CONSUMO_GKWH, marker='^', color='green', label='Consumo Motor 2')
            ax1.scatter(self.ROTACAO_EQUILIBRADA, self.CONSUMO_EQUILIBRADO_GKWH, marker='*', color='green', label='Consumo Equilibrado')
            plt.subplots_adjust(bottom=0.15)
            plt.title(f'Eq Carga - Consumo / Potência x Rotação  {self.caixadatamotores.cget("text")}')
            plt.ylim(150, 250)

            ax2 = ax1.twinx()

            ax2.set_ylabel('Potência (kW)', color='r')
            ax2.plot(x, y, color='r', label='Curva de Potência Ideal')
            ax2.tick_params(axis='y', labelcolor='r')

            ax2.scatter(self.E1_ROTACAO_RPM, self.E1_POTENCIA_KW, marker='s', color='red', label='Potência Motor 1')
            ax2.scatter(self.E2_ROTACAO_RPM, self.E2_POTENCIA_KW, marker='^', color='red', label='Potência Motor 2')
            ax2.scatter(self.ROTACAO_EQUILIBRADA, self.POTENCIA_EQUILIBRADA, marker='*', color='red', label='Potência Equilibrada')

            # Adicionando legendas
            ax1.legend(loc='upper left')
            ax2.legend(loc='upper right')
            self.atualfig=fig
            self.atualtoolbar=toolbar
            self.relatorio_mot_eq=f'''
Equilíbrio de Carga

Rotação Motor 1: {str(round(self.E1_ROTACAO_RPM,2))} rpm
Potência Motor 1: {str(round(self.E1_POTENCIA_KW,2))} kW
Rotação Motor 2: {str(round(self.E2_ROTACAO_RPM,2))} rpm
Potência Motor 2: {str(round(self.E2_POTENCIA_KW,2))} kW
Rotação Equilibrada: {str(round(self.ROTACAO_EQUILIBRADA,2))} rpm
Potência Equilibrada: {str(round(self.POTENCIA_EQUILIBRADA,2))} kW'

Análise


{analise_equilibrio}'''

    def relatorio_motores(self):
            data=self.data_escrita()[1].replace(''':''',"-").replace(" ","--------------")
            name_i=f"Relatório {data}.txt"
            file=filedialog.asksaveasfilename(title="Escolha o local para salvar o relatório.",filetypes=[("TXT",".txt")],initialfile=name_i)
            if file =="":
                return
            if not ".txt" in file:
                file+=".txt"

            with open(file,'w',encoding = 'utf-8') as relatorio:
                textos=f'''

{self.relatorio_mot_geral} 

{self.relatorio_mot_1}
{self.relatorio_mot_2}
{self.relatorio_mot_eq}.'''
                relatorio.write(textos)

            os.startfile(file)
    
    def todos_graficos_motores(self,w=None):
        self.data1 = str(self.caixadatamotores.cget("text"))
        self.linha_motor = self.df_dadosnovos[self.df_dadosnovos["DATA E HORA"] == self.data1]
        if w!=None:

            if w==0:
                self.grafico_mot_selected=1
            if w==1:
                self.grafico_mot_selected+=1
            if w==2:
                self.grafico_mot_selected-=1

            if self.grafico_mot_selected==0:
                self.grafico_mot_selected=4

            if self.grafico_mot_selected==5:
                self.grafico_mot_selected=1

        try:
            self.grafico_mot_selected*1
        except:
            self.grafico_mot_selected=1

        botaorelatório=tk.Button(self.frame_equilibrio_carga,text="Salvar relatório",command=self.relatorio_motores).place(x=322,y=95,width=80,height=22)
        

        listcommands= [
            self.analise_motor1,
            self.analise_motor2,
            self.equilibrio_carga,
            self.rota_motores]
        
        for command in listcommands:
            command()
  

        self.entry_grafico_selected_motores.config(textvariable=tk.StringVar(self.master,value=self.grafico_mot_selected))
        listcommands[self.grafico_mot_selected-1]()
        
    def rota_motores(self):
        self.frame_grafico_motor1.destroy()
        self.frame_grafico_motor1 = Frame(self.tbAnaliseMotores)
        self.frame_grafico_motor1.place(x =550 ,y = 80,width = self.largura_grafico,height = self.altura_grafico)
        try:
            if self.data1==self.old_data:
                    label_rota=Label(master=self.frame_grafico_motor1,image=self.img_rota_motores)
                    label_rota.pack()
            else:
                    img_file=self.mapas_rotas.gera_mapa_pontos(self.lon_navio,self.lat_navio,self.direcao_navio,rota=self.rota)
                    img=Image.open(img_file).resize((700,530)).save(img_file)
                    self.img_rota_motores=PhotoImage(master=self.master,file=img_file)
                    self.old_data=self.data1
        except:
                    img_file=self.mapas_rotas.gera_mapa_pontos(self.lon_navio,self.lat_navio,self.direcao_navio,rota=self.rota)
                    img=Image.open(img_file).resize((700,530)).save(img_file)
                    self.img_rota_motores=PhotoImage(master=self.master,file=img_file)
                    self.old_data=self.data1

    def todastendenciasativas(self,w=None):

        self.figurasatuais=[]
        try:
                self.grafico_ten_selected*1
        except:
            self.grafico_ten_selected=1

        if w==0:
            self.grafico_ten_selected=1
        if w==1:
            self.grafico_ten_selected+=1
        if w==2:
            self.grafico_ten_selected-=1

        if self.grafico_ten_selected==0:
            self.grafico_ten_selected=4

        if self.grafico_ten_selected==5:
            self.grafico_ten_selected=1

        if w==10:
            None


        data_inicio = str(self.caixadata_hora_tendencia_consumo_inicio.cget("text"))
        data_final = str(self.caixadata_hora_tendencia_consumo_final.cget("text"))

        data_inicio =dt.strptime(data_inicio, '%m/%d/%Y %H:%M').timestamp()* 1e9 #transforma a data para nano segundos. 
        data_final=dt.strptime(data_final, '%m/%d/%Y %H:%M').timestamp()* 1e9
        (data_inicio,data_final)=sorted((data_inicio,data_final))

        self.intervalo_tendencia = self.df_dadosnovos[
            (data_inicio <= self.df_dadosnovos["DATA ms"]) & 
            (data_final >= self.df_dadosnovos["DATA ms"])
        ]

        listcommands= [
            self.tendencia_consumo,
            self.tendencia_velocidade,
            self.tendencia_onda,
            self.tendencia_vento]
        self.entry_grafico_selected.config(textvariable=tk.StringVar(self.master,value=self.grafico_ten_selected))
        listcommands[self.grafico_ten_selected-1]()

    def tendencias_percursos(self,event=None):

        self.figurasatuais=[]

        inicio=self.inicio_tendencia.get()
        fim=self.fim_tendencia.get()
        new_finals=[]
        if inicio != "":
            for point in self.points:
                if point[0]==inicio:
                    if point[1] != inicio:
                        if not point[1] in new_finals:
                            new_finals.append(point[1])

            self.fim_tendencia.config(values=new_finals)

        cond=False
        if fim != "":
            for point in self.points:
                if point[0]==inicio:
                    if point[1] == fim:
                        cond=True
            if not cond:
                for point in self.points:
                    if point[0]==inicio:
                        if point[1] != fim:  
                            if point[1]!=inicio:
                                self.fim_tendencia.set(point[1])
                                return


        inicio=self.inicio_tendencia.get()
        fim=self.fim_tendencia.get()

        if inicio == "" or fim =="" or fim==inicio :
            return 
        self.master.update()
        tempo,motor1,motor2,tempo_viagem=gera_percu(inicio,fim)
        self.intervalo_tendencia=pd.DataFrame()
        self.intervalo_tendencia["DATA E HORA"]=tempo

        plt,ax1,fig,canvas,toolbar=criagrafico(master=self.framegraficostendecia).geragrafico()
        ax2 = ax1.twinx()

        ax1.plot(tempo,motor1)
        ax1.plot(tempo,motor2)

        title_plot=f"Análise de Tendência por Percurso  Ponto Início:{inicio} - Ponto Final: {fim}"
        plt.title(title_plot,fontsize=12)

        ax1.set_ylabel('Consumo Total [g] ', color='orange')
        ax1.scatter(tempo,motor1)
        ax1.scatter(tempo,motor2)
        plt.xticks(rotation=90)
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)
        self.scroll_x_graficoz()
        self.atualfig=fig
        self.atualtoolbar=toolbar
 


    def segundo_plano_video(self):
        a=threading.Thread(target=self.video_rota)
        a.start()

    def video_rota(self):
        import imageio
        r=messagebox.askokcancel(title="Aviso",message="Deseja carregar o video da rota ?")
        self.lista_frames=[]
        if r:            
            self.mapas_rotas.gera_frames(self.intervalo_tendencia,lim_frames=200)
            arqs=os.listdir("Frames")
            escritor=imageio.get_writer("teste.mp4",fps=20)
            for i in range(0,len(arqs)):
                    arq=f"Frames\Frame {i}.png"
                    #print(arq)
                    escritor.append_data(imageio.imread(arq))
            escritor.close()
                    #self.lista_frames.append(current_image)
        #self.lista_frames[0].save('pillow_imagedraw.gif',
                #save_all = True, append_images = self.lista_frames[1:], 
                #optimize = False, duration = 60)
            os.startfile("teste.mp4")
                    

                
            
        #self.iii=PhotoImage(master=self.master,file=self.image_calendario_geral)
        #label=Label(master=self.framegraficostendecia,image=self.iii)
        #label.pack()
   
    def tendencia_consumo(self):
        
        self.intervalo_tendencia["E1_CONSUMO_KGH"]  = self.intervalo_tendencia["E1_CONSUMO_GH"]/1000
        self.intervalo_tendencia["E2_CONSUMO_KGH"]  = self.intervalo_tendencia["E2_CONSUMO_GH"]/1000

        plt,ax,fig,canvas,toolbar=criagrafico(master=self.framegraficostendecia).geragrafico()
        plt.plot(self.intervalo_tendencia["DATA E HORA"],self.intervalo_tendencia["E1_CONSUMO_KGH"],'b')
        plt.plot(self.intervalo_tendencia["DATA E HORA"],self.intervalo_tendencia["E2_CONSUMO_KGH"],'r')
        plt.title('Consumo x Tempo',fontsize=12)
        plt.ylabel('Consumo .10^3 (g/h)',fontsize=8)
        plt.legend(['Motor 1','Motor 2'],fontsize=8)
        self.scroll_x_graficoz()
        self.atualfig=fig
        self.atualtoolbar=toolbar

    def tendencia_velocidade(self):

        plt,ax,fig,canvas,toolbar=criagrafico(master=self.framegraficostendecia).geragrafico()
        plt.plot(self.intervalo_tendencia["DATA E HORA"],self.intervalo_tendencia["VESSEL_KNOTS"],'b')
        plt.title('Velocidade de Serviço x Tempo',fontsize=12)
        plt.ylabel('Velocidade (nós)',fontsize=8)

        self.scroll_x_graficoz()
        self.atualfig=fig
        self.atualtoolbar=toolbar   
    #Definição da função atrelada ao botão de tendência de altura de onda ao longo do tempo
    def tendencia_onda(self):
        plt,ax,fig,canvas,toolbar=criagrafico(master=self.framegraficostendecia).geragrafico()
        plt.plot(self.intervalo_tendencia["DATA E HORA"],self.intervalo_tendencia["SIG_WAVE_HEIGHT_M"],'b')
        plt.title('Altura de Onda x Tempo',fontsize=12)
        plt.ylabel('Altura de Onda (m)',fontsize=8)
        self.scroll_x_graficoz()
        self.atualfig=fig
        self.atualtoolbar=toolbar
    #Definição da função atrelada ao botão de tendência de velocidade do vento ao longo do tempo
    def tendencia_vento(self):
        plt,ax,fig,canvas,toolbar=criagrafico(master=self.framegraficostendecia).geragrafico()
        plt.plot(self.intervalo_tendencia["DATA E HORA"],self.intervalo_tendencia["WIND_SPEED_M_PER_S"],'b')
        plt.title('Velocidade do Vento x Tempo',fontsize=12)
        plt.ylabel('Velocidade do Vento (m/s)',fontsize=8)
        self.scroll_x_graficoz()
        self.atualfig=fig
        self.atualtoolbar=toolbar

    def carregar_tela_threading(self):
        a=threading.Thread(target=self.telacarregando,args=(self.carregandotela,))
        a.start()

    def carregar_dados(self):
        self.dadoscarregados=False
        self.carregar_tela_threading()
        a=carregar().carregar_dados()
        if a==1:
            self.dadoscarregados=True
            return
        
        lista=os.listdir()
        r = messagebox.askyesno('Adicionar novos dados?',
                                '[Yes] Para adicionar novos dados aos dados antigos\n\n[No] Para começar do zero e EXCLUIR dados antigos')

        if r:
            if "Dados.json" in lista:
                self.completatabela()
                self.dadoscarregados=True
                return
        else:
            r=messagebox.askyesno('ATENÇÃO',"Você selecionou a opção para começar do ZERO e excluir os dados antigos tratados\nDeseja continuar?")
            if not r:
                if "Dados.json" in lista:
                    self.completatabela()
                    self.dadoscarregados=True
                    return
            try:
                dad=pd.read_json("Dados_tratados.json")
            except:
                messagebox.showerror("Erro","Não existe dados tratados. Favor adicionar novos dados")

            dad.to_json("Dados.json")
            r=messagebox.askyesno("Atenção", "Uma nova base de dados foi gerada, deseja gerar uma planilha excel com esses dados?" )
            if r:
                dad.to_csv("Dados.csv")  
                d=filedialog.asksaveasfile(title="Selecione diretório para salvar a planilha")
                if d=="":
                    messagebox.showinfo("Atenção", "Nenhum diretório foi selecionado. Planilha [Dados.xlsx] foi gerada no diretório de origem do programa")
                else:
                    dad.to_excel(d)

            
            self.dadoscarregados=True


            

    def completatabela(self):
        dados=pd.read_json("Dados.json")
        dados2=pd.read_json("Dados_tratados.json")

        df = pd.concat([dados, dados2], ignore_index=True)
        df = df.sort_values(by='DATA ms')
        df=df.drop_duplicates(subset="DATA ms",keep="first")
        df.to_json('Dados.json')

        self.dadoscarregados=True
        self.abre_dados_tratados()


    def colocarfundo(self,master,image,width,height,bd="#555555",esp=0,rel='solid',compond='center'):

        image_pil=Image.open(image)
        image=PhotoImage(file=image,master=self.master)
        self.imagens_fundo.append(image)
        n=len(self.imagens_fundo)
       
        label=Label(master=master,
                    image=self.imagens_fundo[n-1],
                    text="",
                    compound=compond,
                    fg="white",
                    font=("Helvetica",10),
                    background=bd,
                    relief=rel,
                    borderwidth=esp)
        label.pack()

        return label
        # o codigo roda sem erro, porém a imagem não é inserida no frame. 
        # se o parametro "image" já for um objeto PhotoImage, a função funciona normal, mas isso não pode acontecer pq preciso dar o resize 
    def exportar_dados(self):
        if self.dadoscarregados:
            self.dadoscarregados = False

            def exportar():
                file = filedialog.asksaveasfilename(title="Selecione a pasta para salvar a planilha", filetypes=[("EXCEL", ".xlsx")])
                #print(file)
                if file == "":
                    return

                if not file.endswith(".csv"):
                    file = file + ".csv"
                
                self.carregar_tela_threading()
                self.df_dadosnovos.to_csv(file)
                self.dadoscarregados = True
                messagebox.showinfo("Sucesso","Os dados foram exportados com sucesso")
                os.startfile(file)

            exportar_thread = threading.Thread(target=exportar)
            exportar_thread.start()

    def gerainterface(self):
        interface=self.master
        self.nb = ttk.Notebook(self.master)
        self.nb.place(x = 0,y = 0)
        self.nb.pack(fill=tk.BOTH, expand=True,ipady=10)
        self.tbInicio = Frame(self.nb)
        self.tbPercursos = Frame(self.nb)
        self.tbAnaliseMotores = Frame(self.nb)
        self.tbComparacaoMotores = Frame(self.nb)
        self.tbTendenciaConsumo = Frame(self.nb)
        self.tbPredicaoConsumo = Frame(self.nb)
        self.tbPredicaoVelocidade = Frame(self.nb)
        self.tbOtimizacaoConsumo = Frame(self.nb)
        self.nb.add(self.tbInicio,text = "Início")
        self.nb.add(self.tbPercursos,text = "Percursos")
        self.nb.add(self.tbAnaliseMotores,text = "Análise de Motores")
        self.nb.add(self.tbTendenciaConsumo,text = "Análise de Tendência")
        self.nb.add(self.tbPredicaoConsumo,text = "Predição de Consumo")
        self.nb.add(self.tbPredicaoVelocidade,text = "Predição de Velocidade")
        self.nb.add(self.tbOtimizacaoConsumo,text = "Otimização de Consumo")
        
        lblCabecalho = Label(interface,text = 'PROJETO CNPQ EFICIÊNCIA ENERGÉTICA',font = 16,justify="center")
        lblCabecalho.place(x = self.largura_tela/2-360/2,y = 40,width=460)


        ano = date.today().year

        frameCreditos = Frame(self.tbInicio)
        frameCreditos.place(x = self.largura_tela/2-330,y = 130,width = 600,height = 230)
        self.colocarfundo(frameCreditos,self.image_copyright,600,230)

        menu_bar = tk.Menu(interface)
        interface.config(menu=menu_bar)

        menu_arquivo = Menu(menu_bar,tearoff=0)
        menu_ferramentas = Menu(menu_bar,tearoff=0)
        menu_treinamento = Menu(menu_bar,tearoff=0)
        menu_ajuda = Menu(menu_bar,tearoff=0)

        # Adicionar os menus à barra de menu
        menu_bar.add_cascade(label="Arquivo", menu=menu_arquivo)
        menu_bar.add_cascade(label="Ferramentas", menu=menu_ferramentas)
        menu_bar.add_cascade(label="Treinamento", menu=menu_treinamento)
        menu_bar.add_cascade(label="Ajuda", menu=menu_ajuda)
        

        menu_arquivo.add_command(label="Adicionar novos dados", command=self.theread_abre_dados_novos)
        menu_arquivo.add_command(label="Atualizar dados", command=self.theread_abre_dados_tratados)
        menu_arquivo.add_command(label="Exportar dados", command=self.exportar_dados)

        menu_ferramentas.add_command(label="Alterar tipo do mapa")
        menu_ferramentas.add_command(label="Alterar cor de fundo")

        menu_treinamento.add_command(labe="Sobre")
        menu_treinamento.add_command(labe="Treinar para velocidade")
        menu_treinamento.add_command(labe="Treinar para consumo")

        menu_ajuda.add_command(label="Sobre")
        menu_ajuda.add_command(label="Contatos")
        # Adicione os outros comandos para os outros menus, se necessário

        # Coloque o label de carregamento centralizado
        self.carregandotela = Label(self.tbInicio, text='', justify="center")
        self.carregandotela.place(x=self.largura_tela/2-125, y=400, width=250)


        '''
        fonteinicio=("Arial", 9)
        lblCreditos = Label(frameCreditos,text = '(c) Copyright LEDAV-UFRJ, 2023-'+str(ano),font=fonteinicio,width=200)
        lblCreditos.place(x = self.largura_tela/2-100,y = 90)

        lblAutor0 = Label(frameCreditos,text = 'Kaléo Elias Gonçalves da Silva',font=fonteinicio)
        lblAutor0.place(x = 15,y = 60)

        lblEmail1 = Label(frameCreditos,text = 'kaleonaval.20221@poli.ufrj.br',font=fonteinicio)
        lblEmail1.place(x = 220,y = 60)

        lblAutor1 = Label(frameCreditos,text = 'Marlon Barrêto Silva',font=fonteinicio)
        lblAutor1.place(x = 15,y = 90)

        lblEmail1 = Label(frameCreditos,text = 'marlon.barreto1201@poli.ufrj.br',font=fonteinicio)
        lblEmail1.place(x = 220,y = 90)
                          
        lblAutor2 = Label(frameCreditos,text = 'Prof. Luiz Antonio Vaz Pinto',font=fonteinicio)
        lblAutor2.place(x = 15,y = 120)

        lblEmail2 = Label(frameCreditos,text = 'vaz@oceanica.ufrj.br',font=fonteinicio)
        lblEmail2.place(x = 220,y = 120)

        lblAutor3 = Label(frameCreditos,text = 'Prof. Luiz Augusto Baptista',font=fonteinicio)
        lblAutor3.place(x = 15,y = 150)

        lblEmail3 = Label(frameCreditos,text = 'laugustorb@oceanica.ufrj.br',font=fonteinicio)
        lblEmail3.place(x = 220,y = 150)
        '''

        #self.carregar_dadosButton = Button(self.tbInicio,text = 'Adicionar novos dados',command = self.theread_abre_dados_novos)
        #self.carregar_dadosButton.place(x = self.largura_tela/2-125,y = 460,width=250)
        
        #self.carregar_dadosButton = Button(self.tbInicio,text = 'Atualizar dados',command =self.theread_abre_dados_tratados)
        #self.carregar_dadosButton.place(x = self.largura_tela/2-125,y = 370,width=250)

        #menu_arquivo.add_command(label="Salvar como...", command=salvar_como)
        #menu_arquivo.add_separator()
        #menu_arquivo.add_command(label="Abrir", command=abrir)

        #Montagem da aba de percursos
        #OH HOLD
        width,height=530,400
        escala=0.7
        self.largura_grafico,self.altura_grafico=int(self.largura_tela*escala),int(self.altura_tela*escala)
        
        self.frame_grafico_perc = Frame(self.tbPercursos)
        self.frame_grafico_perc.place(x =300 ,y = 80,width = self.largura_grafico,height = self.altura_grafico)
        
        self.frame_texto_perc=Frame(self.tbPercursos)
        self.frame_texto_perc.place(x=20,y=50,width=250,height=630)
        self.label_text_info=self.colocarfundo(self.frame_texto_perc,self.image_percurso_info,180,350)

        self.titulos_number_select=["VESSEL_KNOTS", "WIND_SPEED_M_PER_S","E1_CONSUMO_GH","E2_CONSUMO_GH","E1_POTÊNCIA_KW","E2_POTÊNCIA_KW","E1_ROTAÇÃO_RPM","E2_ROTAÇÃO_RPM","TEMPERATURE_C"]
        self.titulos_capa=["Velocidade do Navio (Nós)", "Velocidade do Vento (m/s)", "Consumo Motor 1 (g/h)", "Consumo Motor 2 (g/h)", "Potência Motor 1 (kW)", "Potência Motor 2 (kW)", "RPM Motor 1", "RPM Motor 2","Temperatura Ambiente (C°)"]
        self.bombox_percurso_titulo=ttk.Combobox(self.frame_texto_perc,values=self.titulos_capa,justify="center",state="readonly")
        
        Label(master=self.frame_texto_perc,text="Selecionar parâmetro").place(x=47,y=140,width=160)
        self.bombox_percurso_titulo.place(x=47,y=160,width=160) 
        self.bombox_percurso_titulo.bind("<<ComboboxSelected>>",self.func_percurso)
        inicios=[]
        finais=[]
        self.points=[]

        Label(master=self.frame_texto_perc,text="Selecione o ponto incial").place(x=47,y=40,width=160)
        self.inicio_tendencia2=ttk.Combobox(self.frame_texto_perc,values=inicios,justify="center",state="readonly")
        self.inicio_tendencia2.place(x=47,y=60,width=160)
        self.inicio_tendencia2.bind("<<ComboboxSelected>>",self.func_percurso)

        Label(master=self.frame_texto_perc,text="Selecione o ponto final").place(x=47,y=80,width=160)
        self.fim_tendencia2=ttk.Combobox(self.frame_texto_perc,values=finais,justify="center",state="readonly")
        self.fim_tendencia2.place(x=47,y=100,width=160) 
        self.fim_tendencia2.bind("<<ComboboxSelected>>",self.func_percurso)
        self.label_text_info.config(text='-',justify="left")
        
        #Montagem da aba de análise de motores  
        b=0
        self.frame_calendario_motores = Frame(self.tbAnaliseMotores,borderwidth=b,relief='solid')
        self.frame_calendario_motores.place(x = 146,y = 15,width = 240,height = 175)
        self.colocarfundo(self.frame_calendario_motores,self.image_calendario_motores,600,230)
        self.fundoazul=PhotoImage(file=self.image_fundo_azul,master=self.master)
        self.caixadatamotores=Label(master=self.frame_calendario_motores,text="NÃO SELECIONADA",compound='center',justify="center",font=("Arial", 12),foreground="white",background="black",image=self.fundoazul)
        self.caixadatamotores.place(x=25,y=105,width=190,height=20)
        self.caixadata_hora = Button(self.frame_calendario_motores,text="Selecionar Data",command=lambda:self.dataselected(self.tbAnaliseMotores,self.caixadatamotores),image=self.calendarioicon,highlightthickness=0,border=0,bd=3,background=self.rgb_to_color((10,46,62)))
        self.caixadata_hora.place(x = 120-25, y = 43,width=54,height=50)
        
        

        cc=17
        self.frame_analise_geral= Frame(self.tbAnaliseMotores,borderwidth=b,relief='solid')
        self.frame_analise_geral.place(x = 146,y = 170,width = 240,height = 140)
        self.label_info_geral=self.colocarfundo(self.frame_analise_geral,image=self.imagemotoresgeral,width = 230,height = 240)

        self.frame_analise_motor1 = Frame(self.tbAnaliseMotores,borderwidth=b,relief='solid')
        self.frame_analise_motor1.place(x = 30,y = 291+cc,width = 230,height = 150)
        self.label_info_motor1=self.colocarfundo(self.frame_analise_motor1,image=self.imagemotor1,width = 230,height = 240)

        self.frame_analise_motor2 = Frame(self.tbAnaliseMotores,borderwidth=b,relief='solid')
        self.frame_analise_motor2.place(x = 270,y =291+cc,width = 230,height = 150)
        self.label_info_motor2=self.colocarfundo(self.frame_analise_motor2,image=self.imagemotor2,width = 230,height = 240)

        self.frame_equilibrio_carga = Frame(self.tbAnaliseMotores,borderwidth=b,relief='solid')
        self.frame_equilibrio_carga.place(x = 22,y = 428+cc,width = 480,height = 150)
        self.label_info_equilibrio=self.colocarfundo(self.frame_equilibrio_carga,self.image_equilibrio,600,230)
        
        self.frame_grafico_motor1 = Frame(self.tbAnaliseMotores,borderwidth = b)
        self.frame_grafico_motor1.place(x =550 ,y = 80,width = self.largura_grafico,height = self.altura_grafico)

        motores_grafico_select_frame=tk.Frame(self.tbAnaliseMotores)
        motores_grafico_select_frame.place(x=215,y=580,width=104)
        button_select_grafico_left_motores=tk.Button(motores_grafico_select_frame,command=lambda:self.todos_graficos_motores(2),text="<-",image=self.setaesquerdaicon,highlightthickness=0,border=0).pack(side="left",padx=0)
        self.entry_grafico_selected_motores=tk.Entry(motores_grafico_select_frame,textvariable=tk.StringVar(self.master,value="-"),width=3,justify="center",state="readonly",fg="black")
        self.entry_grafico_selected_motores.pack(side="left")
        button_select_grafico_right_motores=tk.Button(motores_grafico_select_frame,command=lambda:self.todos_graficos_motores(1),text="->",image=self.setadireitaicon,highlightthickness=0,border=0).pack(side="right",padx=0)
        self.grafico_mot_selected=1
       

        #análise de tendência
        self.tendencias_percurso=False
        self.tendencias_data=False
        self.tend=tendencias(self)
 
        #self.button_data=Button(self.tbTendenciaConsumo,text="ÁNALISE POR DATA",command=self.cria_tendencia_data)
        #self.button_data.place(x=20,y=120,width=150,height=150)

        #self.button_percurso=Button(self.tbTendenciaConsumo,text="ÁNALISE POR PERCURSO",command=self.cria_tendencia_percurso)
        #self.button_percurso.place(x=20,y=300,width=150,height=150)



        #Montagem da aba de predição de consumo
        self.frame_predicao_de_consumo = Frame(self.tbPredicaoConsumo,borderwidth = 1,relief = 'solid')
        self.frame_predicao_de_consumo.place(x = 215,y = 105,width = 400,height = 310)
        
        self.lblpredicao_predicao_de_consumo = Label(self.tbPredicaoConsumo,text = '  Predição de Consumo  ')
        self.lblpredicao_predicao_de_consumo.place(x = 351,y = 95)

        self.lblaltura_onda_predicao_consumo = Label(self.frame_predicao_de_consumo,text = "Informe altura de onda (m)")
        self.lblaltura_onda_predicao_consumo.place(x = 18,y = 15)
        self.caixaaltura_onda_predicao_consumo = Entry(self.frame_predicao_de_consumo)
        self.caixaaltura_onda_predicao_consumo.place(x = 28, y = 35)

        self.lblvelocidade_vento_predicao_consumo = Label(self.frame_predicao_de_consumo,text = "Informe velocidade do vento (m/s)")
        self.lblvelocidade_vento_predicao_consumo.place(x = 3,y = 65)
        self.caixavelocidade_vento_predicao_consumo = Entry(self.frame_predicao_de_consumo)
        self.caixavelocidade_vento_predicao_consumo.place(x = 28, y = 85)

        self.lblpotencia1_predicao_consumo = Label(self.frame_predicao_de_consumo,text = "Informe potência do motor 1 (kW)")
        self.lblpotencia1_predicao_consumo.place(x = 3,y = 115)
        self.caixapotencia1_predicao_consumo = Entry(self.frame_predicao_de_consumo)
        self.caixapotencia1_predicao_consumo.place(x = 28, y = 135)

        self.lblrotacao1_predicao_consumo = Label(self.frame_predicao_de_consumo,text = "Informe rotação do motor 1 (rpm)")
        self.lblrotacao1_predicao_consumo.place(x = 3,y = 165)
        self.caixarotacao1_predicao_consumo = Entry(self.frame_predicao_de_consumo)
        self.caixarotacao1_predicao_consumo.place(x = 28, y = 185)

        self.lbldirecao_vento_predicao_consumo = Label(self.frame_predicao_de_consumo,text = "Informe direção do vento (°)")
        self.lbldirecao_vento_predicao_consumo.place(x = 216,y = 15)
        self.caixadirecao_vento_predicao_consumo = Entry(self.frame_predicao_de_consumo)
        self.caixadirecao_vento_predicao_consumo.place(x = 228, y = 35)

        self.lbltemperatura_ambiente_predicao_consumo = Label(self.frame_predicao_de_consumo,text = "Informe temperatura ambiente (°C)")
        self.lbltemperatura_ambiente_predicao_consumo.place(x = 199,y = 65)
        self.caixatemperatura_ambiente_predicao_consumo = Entry(self.frame_predicao_de_consumo)
        self.caixatemperatura_ambiente_predicao_consumo.place(x = 228, y = 85)

        self.lblpotencia2_predicao_consumo = Label(self.frame_predicao_de_consumo,text = "Informe potência do motor 2 (kW)")
        self.lblpotencia2_predicao_consumo.place(x = 203,y = 115)
        self.caixapotencia2_predicao_consumo = Entry(self.frame_predicao_de_consumo)
        self.caixapotencia2_predicao_consumo.place(x = 228, y = 135)

        self.lblrotacao2_predicao_consumo = Label(self.frame_predicao_de_consumo,text = "Informe rotação do motor 2 (rpm)")
        self.lblrotacao2_predicao_consumo.place(x = 203,y = 165)
        self.caixarotacao2_predicao_consumo = Entry(self.frame_predicao_de_consumo)
        self.caixarotacao2_predicao_consumo.place(x = 228, y = 185)

        self.lblvelocidade_predicao_consumo = Label(self.frame_predicao_de_consumo,text = "Informe velocidade de serviço (nós)")
        self.lblvelocidade_predicao_consumo.place(x = 112,y = 210)
        self.caixavelocidade_predicao_consumo = Entry(self.frame_predicao_de_consumo)
        self.caixavelocidade_predicao_consumo.place(x = 140, y = 230)

        #self.predicao_de_consumoButton = Button(self.frame_predicao_de_consumo,text = 'PREDIÇÃO',command =lambda: rede().predicao_de_consumo(self,treino=False),width = 10)
        #self.predicao_de_consumoButton.place(x = 130,y = 255)

        #self.treinar_de_consumoButton = Button(self.frame_predicao_de_consumo,text = 'TREINAR',command =lambda: rede().predicao_de_consumo(self,treino=True),width = 10)
        #self.treinar_de_consumoButton.place(x = 210,y = 255)

        # predição de velocidade


        self.frame_predicao_de_velocidade = Frame(self.tbPredicaoVelocidade,borderwidth = 1,relief = 'solid')
        self.frame_predicao_de_velocidade.place(x = 215,y = 105,width = 400,height = 310)
        
        self.lblpredicao_predicao_de_velocidade = Label(self.tbPredicaoVelocidade,text = '  Predição de velocidade  ')
        self.lblpredicao_predicao_de_velocidade.place(x = 351,y = 95)

        self.lblaltura_onda_predicao_velocidade = Label(self.frame_predicao_de_velocidade,text = "Informe altura de onda (m)")
        self.lblaltura_onda_predicao_velocidade.place(x = 18,y = 15)
        self.caixaaltura_onda_predicao_velocidade = Entry(self.frame_predicao_de_velocidade)
        self.caixaaltura_onda_predicao_velocidade.place(x = 28, y = 35)

        self.lblvelocidade_vento_predicao_velocidade = Label(self.frame_predicao_de_velocidade,text = "Informe velocidade do vento (m/s)")
        self.lblvelocidade_vento_predicao_velocidade.place(x = 3,y = 65)
        self.caixavelocidade_vento_predicao_velocidade = Entry(self.frame_predicao_de_velocidade)
        self.caixavelocidade_vento_predicao_velocidade.place(x = 28, y = 85)

        self.lblpotencia1_predicao_velocidade = Label(self.frame_predicao_de_velocidade,text = "Informe potência do motor 1 (kW)")
        self.lblpotencia1_predicao_velocidade.place(x = 3,y = 115)
        self.caixapotencia1_predicao_velocidade = Entry(self.frame_predicao_de_velocidade)
        self.caixapotencia1_predicao_velocidade.place(x = 28, y = 135)

        self.lblrotacao1_predicao_velocidade = Label(self.frame_predicao_de_velocidade,text = "Informe rotação do motor 1 (rpm)")
        self.lblrotacao1_predicao_velocidade.place(x = 3,y = 165)
        self.caixarotacao1_predicao_velocidade = Entry(self.frame_predicao_de_velocidade)
        self.caixarotacao1_predicao_velocidade.place(x = 28, y = 185)

        self.lbldirecao_vento_predicao_velocidade = Label(self.frame_predicao_de_velocidade,text = "Informe direção do vento (°)")
        self.lbldirecao_vento_predicao_velocidade.place(x = 216,y = 15)
        self.caixadirecao_vento_predicao_velocidade = Entry(self.frame_predicao_de_velocidade)
        self.caixadirecao_vento_predicao_velocidade.place(x = 228, y = 35)

        self.lbltemperatura_ambiente_predicao_velocidade = Label(self.frame_predicao_de_velocidade,text = "Informe temperatura ambiente (°C)")
        self.lbltemperatura_ambiente_predicao_velocidade.place(x = 199,y = 65)
        self.caixatemperatura_ambiente_predicao_velocidade = Entry(self.frame_predicao_de_velocidade)
        self.caixatemperatura_ambiente_predicao_velocidade.place(x = 228, y = 85)

        self.lblpotencia2_predicao_velocidade = Label(self.frame_predicao_de_velocidade,text = "Informe potência do motor 2 (kW)")
        self.lblpotencia2_predicao_velocidade.place(x = 203,y = 115)
        self.caixapotencia2_predicao_velocidade = Entry(self.frame_predicao_de_velocidade)
        self.caixapotencia2_predicao_velocidade.place(x = 228, y = 135)

        self.lblrotacao2_predicao_velocidade = Label(self.frame_predicao_de_velocidade,text = "Informe rotação do motor 2 (rpm)")
        self.lblrotacao2_predicao_velocidade.place(x = 203,y = 165)
        self.caixarotacao2_predicao_velocidade = Entry(self.frame_predicao_de_velocidade)
        self.caixarotacao2_predicao_velocidade.place(x = 228, y = 185)

        self.lblvelocidade_predicao_velocidade = Label(self.frame_predicao_de_velocidade,text = "Informe o consumo do motor 1")
        self.lblvelocidade_predicao_velocidade.place(x = 3,y = 210)
        self.caixaconsumo_predicao_velocidade = Entry(self.frame_predicao_de_velocidade)
        self.caixaconsumo_predicao_velocidade.place(x = 28, y = 230)

        self.lblvelocidade_predicao_velocidade = Label(self.frame_predicao_de_velocidade,text = "Informe o consumo do motor 2")
        self.lblvelocidade_predicao_velocidade.place(x = 216,y = 210)
        self.caixaconsumo_predicao_velocidade = Entry(self.frame_predicao_de_velocidade)
        self.caixaconsumo_predicao_velocidade.place(x = 228, y = 230)

        #self.predicao_de_velocidadeButton = Button(self.frame_predicao_de_velocidade,text = 'PREDIÇÃO',command =lambda: rede().predicao_de_velocidade(self,treino=False),width = 10)
        #self.predicao_de_velocidadeButton.place(x = 130,y = 255)

        #self.treinar_de_velocidadeButton = Button(self.frame_predicao_de_velocidade,text = 'TREINAR',command =lambda: rede().predicao_de_velocidade(self,treino=True),width = 10)
        #self.treinar_de_velocidadeButton.place(x = 210,y = 255)

        x,y=self.largura_tela*0.8,40
        extrairgrafico=Button(self.tbPercursos,text="Extrair Gráfico",command=self.extraigrafico).place(x=x,y=y)
        extrairgrafico=Button(self.tbAnaliseMotores,text="Extrair Gráfico",command=self.extraigrafico).place(x=x,y=y)
        extrairgrafico=Button(self.tbTendenciaConsumo,text="Extrair Gráfico",command=self.extraigrafico).place(x=x,y=y)
        self.percursos()
   
    def novo_treino(self):
        self.botao_treinar_predicao.config(text="Treinar",command=self.treinar_dados)
        self.carregar_titles_predicao.config(text = 'Carregar modelo',command = self.carregar_titulos)
        self.label_predicao_titulos.config(text="")
        self.bombox_predicao_titulo.place(x=100,y=30,width=160)
        self.botao_limpar_predicao.config(text="Limpar escolhas",command=lambda:self.label_predicao_titulos.config(text=""))
    
    def carregar_titulos(self,file=None):
        if file==None:
            file=filedialog.askopenfilename(filetypes=[("KERAS", "*.keras")])
            self.modelo_keras=file
            file=file.replace(".keras",".ledav")
        else:
            self.modelo_keras=file.replace(".ledav",".keras")

        outfile = open(file, 'r')
        titles=outfile.read().split(",")
        texto="\n"
        #print(titles)
        for titulo in titles:
            texto+=titulo+"\n"
        self.label_predicao_titulos.config(text=texto)
        self.botao_treinar_predicao.config(text="Predição",command=self.prever_dados)
        self.bombox_predicao_titulo.place_forget()
        self.botao_limpar_predicao.config(text = 'Novo treino',command = self.novo_treino)


    def adiciona_titulo(self,event):
        titulo=self.bombox_predicao_titulo.get()
        atual=self.label_predicao_titulos.cget("text")
        try:
            listatual=atual.split("\n")
        except:
            listatual=[]
        if titulo in listatual:
            messagebox.showinfo("Atenção","O titulo selecionado já está na lista dos resultados")
            return 
        novo=atual+"\n"+titulo
        self.label_predicao_titulos.config(text=novo)


    def treinar_dados(self):
        atual=self.label_predicao_titulos.cget("text")
        lista=atual.split("\n")[1:]
        if len(lista)==0:
            messagebox.showinfo("Atenção","Selecione pelo menos 1 título")
            return 
       # threading.Thread(target=rede().treinar(lista,self.carregar_titulos)).start()

mastertela=obj.tela_carregamento(100,0)
app = main(mastertela)

        

