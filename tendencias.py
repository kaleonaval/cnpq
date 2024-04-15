from tkinter import ttk
from tkinter import *
import tkinter as tk 
import pandas as pd


class tendencias:
    def __init__(self,selfori):
        self.selfori=selfori
        dados_excel = pd.read_excel("pontos.xlsx")
        self.points=[]
        i=0
        for a in dados_excel.index:
                self.points.append(i)
                i+=1

        self.button_data=Button(self.selfori.tbTendenciaConsumo,text="ANÁLISE POR DATA",command=self.cria_tendencia_data)
        self.button_data.place(x=20,y=20,width=140,height=25)

        self.button_percurso=Button(self.selfori.tbTendenciaConsumo,text="ANÁLISE POR PERCURSO",command=self.cria_tendencia_percurso)
        self.button_percurso.place(x=20+140,y=20,width=140,height=25)


    def cria_tendencia_data(self):
        self.frame=tk.Frame(self.selfori.tbTendenciaConsumo,width=360,height=500)
        self.frame.place(x=10,y=50)

        self.button_data.config(background="White",foreground="black")
        self.button_percurso.config(background=self.selfori.cor_fundo,foreground="white")
        self.selfori.tendencias_percurso=False
        self.selfori.tendencias_data=True


        self.selfori.framedatai = Frame(self.frame)
        self.selfori.framedatai.place(x = 10,y = 20,width = 340,height = 130)
        self.selfori.colocarfundo(self.selfori.framedatai,self.selfori.image_data_inicio,300,100)

        self.selfori.framedatafi = Frame(self.frame)
        self.selfori.framedatafi.place(x = 10,y = 160,width = 340,height = 130)
        self.selfori.colocarfundo(self.selfori.framedatafi,self.selfori.image_data_final,300,100)


        self.selfori.caixadata_hora_tendencia_consumo_inicio = Label(self.selfori.framedatai,justify="center",font=("Arial", 12),fg="black",text="NÃO SELECIONADA",foreground="white",background="black",image=self.selfori.fundoazul,compound="center")
        self.selfori.caixadata_hora_tendencia_consumo_inicio.place(x = 125, y = 61,width=160,height=25)

        self.selfori.lbldata_hora_tendencia_consumo_inicio = Button(self.selfori.framedatai,text = "Informe data e hora iniciais",command=lambda:self.selfori.dataselected(self.selfori.tbTendenciaConsumo,self.selfori.caixadata_hora_tendencia_consumo_inicio),image=self.selfori.calendarioicon,highlightthickness=0,border=0,bd=3,background=self.selfori.rgb_to_color((10,46,62)))
        self.selfori.lbldata_hora_tendencia_consumo_inicio.place(x = 40, y = 40)
        
        self.selfori.caixadata_hora_tendencia_consumo_final =  Label(self.selfori.framedatafi,justify="center",font=("Arial", 12),fg="black",text="NÃO SELECIONADA",foreground="white",background="black",image=self.selfori.fundoazul,compound="center")
        self.selfori.caixadata_hora_tendencia_consumo_final.place(x = 125, y = 61,width=160,height=25)

        self.selfori.lbldata_hora_tendencia_consumo_final = Button(self.selfori.framedatafi,text = "Informe data e hora finais",command=lambda:self.selfori.dataselected(self.selfori.tbTendenciaConsumo,self.selfori.caixadata_hora_tendencia_consumo_final),image=self.selfori.calendarioicon,highlightthickness=0,border=0,bd=3,background=self.selfori.rgb_to_color((10,46,62)))
        self.selfori.lbldata_hora_tendencia_consumo_final.place(x = 40, y = 40)
        larg=850
        alt=530
        xi=410
        yi=80

        self.selfori.framegraficostendecia=Frame(self.selfori.tbTendenciaConsumo)
        self.selfori.framegraficostendecia.place(x=xi,y=yi,width = self.selfori.largura_grafico,height = self.selfori.altura_grafico)
        grafico_tendencia_frame = tk.Frame(self.selfori.tbTendenciaConsumo)
        grafico_tendencia_frame.place(x=145,y=435)#frame que tem as setas
        button_select_grafico_left=tk.Button(grafico_tendencia_frame,command=lambda:self.selfori.todastendenciasativas(2),text="<-",image=self.selfori.setaesquerdaicon,highlightthickness=0,border=0).pack(side="left",padx=0)
        self.selfori.entry_grafico_selected=tk.Entry(master=grafico_tendencia_frame,textvariable=tk.StringVar(self.selfori.master,value="-"),width=3,justify="center",state="readonly",fg="black")
        self.selfori.entry_grafico_selected.pack(side="left")
        button_select_grafico_right=tk.Button(grafico_tendencia_frame,command=lambda:self.selfori.todastendenciasativas(1),text="->",image=self.selfori.setadireitaicon,highlightthickness=0,border=0).pack(side="right",padx=0)
        self.selfori.scalex_scrollbutton=tk.Scale(self.selfori.tbTendenciaConsumo,from_=1,to=100,variable=tk.DoubleVar(value=self.selfori.escala_x_grafico),orient=tk.HORIZONTAL,width=10,sliderlength=20,length=300)
        self.selfori.scalex_scrollbutton.place(x=630,y=self.selfori.altura_grafico+int(yi/2))
        self.selfori.button_video=tk.Button(master=self.frame,text="Gerar video da rota",command=self.selfori.segundo_plano_video)
        self.selfori.button_video.place(x=130,y=300)
        self.selfori.label_load=Label(master=self.selfori.tbTendenciaConsumo)
        self.selfori.label_load.place(x=100,y=480)
        self.selfori.scalex_scrollbutton.bind("<ButtonRelease-1>",self.selfori.scroll_x_graficoz)
        self.selfori.grafico_ten_selected=1

    def cria_tendencia_percurso(self):
        
        self.frame=tk.Frame(self.selfori.tbTendenciaConsumo,width=360,height=500,borderwidth=1,relief="solid")
        self.frame.place(x=10,y=50)

        self.button_data.config(background=self.selfori.cor_fundo,foreground="white")
        self.button_percurso.config(background="White",foreground="black")
        self.selfori.tendencias_percurso=True
        self.selfori.tendencias_data=False
        name_inicio=Label(master=self.frame,text="Selecione o ponto incial").place(x=24+100,y=10,width=160)
        self.selfori.inicio_tendencia=ttk.Combobox(self.frame,values=self.points,justify="center",state="readonly")
        self.selfori.inicio_tendencia.place(x=24+100,y=30,width=160)
        self.selfori.inicio_tendencia.bind("<<ComboboxSelected>>",self.selfori.tendencias_percursos)

        larg=880
        alt=530
        xi=380
        yi=80
        self.selfori.framegraficostendecia=Frame(self.selfori.tbTendenciaConsumo)
        self.selfori.framegraficostendecia.place(x=xi,y=yi,width = self.selfori.largura_grafico,height = self.selfori.altura_grafico)
        self.selfori.scalex_scrollbutton=tk.Scale(self.selfori.tbTendenciaConsumo,from_=1,to=100,variable=tk.DoubleVar(value=self.selfori.escala_x_grafico),orient=tk.HORIZONTAL,width=10,sliderlength=20,length=300)
        self.selfori.scalex_scrollbutton.place(x=630,y=self.selfori.altura_grafico+int(yi/2))
        self.selfori.scalex_scrollbutton.bind("<ButtonRelease-1>",self.selfori.scroll_x_graficoz)
        self.selfori.grafico_ten_selected=1
        name_final=Label(self.frame,text="Selecione o ponto final").place(x=24+100,y=60,width=160)
        self.selfori.fim_tendencia=ttk.Combobox(self.frame,values=self.points,justify="center",state="readonly")
        self.selfori.fim_tendencia.place(x=24+100,y=80,width=160) 
        self.selfori.fim_tendencia.bind("<<ComboboxSelected>>",self.selfori.tendencias_percursos)









class teste:
    def __init__(self):
        interface=Tk()
        interface.geometry("800x600")
        nb = ttk.Notebook(interface)
        tbTendenciaConsumo = Frame(nb)
        nb.add(tbTendenciaConsumo,text = "Análise de Tendência")
        tendencias(tbTendenciaConsumo,interface,self)
        nb.place(x = 0,y = 0)
        nb.pack(fill=tk.BOTH, expand=True,ipady=10)
        interface.mainloop()

    def printoi(self):
        print("oi")

    def cabritão(self):
        print("olaoaloal")



#teste()