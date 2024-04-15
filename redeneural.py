from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import load_model
import tensorflow as tf
import pandas as pd 
import openpyxl
from datetime import datetime 
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *

class rede:
    def __init__(self):

        pass

    def predicao_de_consumo(self,selfori,treino):
        if treino:

            r=messagebox.askyesno(title='Atenção',message='''
Você selecionou a opção de treinamento, esse processo
pode demorar muitas horas ou até dias, dependendo do seu 
banco de dados.

Deseja continuar?''')
            print(r)
            if not r:
                treino=False
            else:
                treino=True
  # Carregando os dados de predição a partir da planilha gerada anteriormente
            # Fazendo previsões em novos dados
            # Salvando dados informados pelo usuário
        
            # Normalização das características (opcional, mas geralmente recomendada)


        selfori.altura_onda = float(selfori.caixaaltura_onda_predicao_consumo.get())
        selfori.velocidade_vento = float(selfori.caixavelocidade_vento_predicao_consumo.get())
        selfori.direcao_vento = float(selfori.caixadirecao_vento_predicao_consumo.get())
        selfori.temperatura_ambiente = float(selfori.caixatemperatura_ambiente_predicao_consumo.get())
        selfori.velocidade = float(selfori.caixavelocidade_predicao_consumo.get())
        selfori.potencia1 = float(selfori.caixapotencia1_predicao_consumo.get())
        selfori.rotacao1 = float(selfori.caixarotacao1_predicao_consumo.get())
        selfori.potencia2 = float(selfori.caixapotencia2_predicao_consumo.get())
        selfori.rotacao2 = float(selfori.caixarotacao2_predicao_consumo.get())
        novos_dados=[[
selfori.altura_onda ,
selfori.velocidade_vento ,
selfori.direcao_vento ,
selfori.temperatura_ambiente ,
selfori.velocidade ,
selfori.potencia1 ,
selfori.rotacao1 ,
selfori.potencia2 ,
selfori.rotacao2 
        ]]

        # Transformando os dados fornecidos pelo usuário num dataframe que será usado para predição

        




        if treino:
            selfori.df_novo = pd.read_excel('Dados.xlsx')
            selfori.df_predicao = pd.DataFrame((selfori.df_novo.SIG_WAVE_HEIGHT_M_COR,selfori.df_novo.WIND_SPEED_M_PER_S_COR,selfori.df_novo.REL_WIND_DIRECTION,selfori.df_novo.TEMPERATURE_C,selfori.df_novo.VESSEL_KNOTS,selfori.df_novo.E1_POTÊNCIA_KW,selfori.df_novo.E1_ROTAÇÃO_RPM,selfori.df_novo.E2_POTÊNCIA_KW,selfori.df_novo.E2_ROTAÇÃO_RPM,selfori.df_novo.E1_E2_CONSUMO_GH,), index=["SIG_WAVE_HEIGHT_M","WIND_SPEED_M_PER_S","WIND_DIRECTION","TEMPERATURE_C","VESSEL_KNOTS","E1_POTÊNCIA_KW","E1_ROTAÇÃO_RPM","E2_POTÊNCIA_KW","E2_ROTAÇÃO_RPM","E1_E2_CONSUMO_GH"]).T

            # Filtrando os dataframes para considerar apenas condições do navio em deslocamento
            filtro = selfori.df_predicao["VESSEL_KNOTS"] >= 2
            selfori.df_predicao = selfori.df_predicao[filtro]

            # Separando as características (X) e os valores de resposta (y)
            x = selfori.df_predicao.iloc[:, :-1].values  # Todas as colunas, exceto a última
            y = selfori.df_predicao.iloc[:, -1].values  # A última coluna

            # Dividindo os dados em conjuntos de treinamento e teste
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

            # Confloatuindo os modelos da rede neural
            model = tf.keras.Sequential([
                tf.keras.layers.Input(shape=(x_train.shape[1],)),  # Camada de entrada com o número de características
                tf.keras.layers.Dense(512, activation='relu'),  # Camada oculta com 512 neurônios e ativação ReLU
                tf.keras.layers.Dense(256, activation='relu'),  # Camada oculta com 256 neurônios e ativação ReLU
                tf.keras.layers.Dense(128, activation='relu'),  # Camada oculta com 128 neurônios e ativação ReLU
                tf.keras.layers.Dense(64, activation='relu'),  # Camada oculta com 64 neurônios e ativação ReLU
                tf.keras.layers.Dense(32, activation='relu'),  # Camada oculta com 32 neurônios e ativação ReLU
                tf.keras.layers.Dense(1)  # Camada de saída com 1 neurônio para regressão
            ])

            
            model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_absolute_error'])
            model.fit(x_train, y_train, epochs=100, batch_size=32, validation_data=(x_test, y_test))
            model.save('modelo_treinado.keras')


        else:
            try:
                model = load_model('modelo_treinado.keras')
            except:
                messagebox.showerror(title='ERRO',message='''
Não existe um modelo treinado para a predição.
Por favor, clique em [TREINAR] para treinar o modelo.''')
           

        previsao = model.predict(novos_dados)
        print(previsao)
        lblPredicaoConsumo = Label(selfori.frame_predicao_de_consumo,text = "PREDIÇÃO DE CONSUMO TOTAL (g/h): " + str(previsao[0][0]) + " g/h")
        lblPredicaoConsumo.place(x = 40,y = 285)

        with open('Relatório.txt','a',encoding = 'utf-8') as relatorio:
            relatorio.write('\n'+'\n'+'\n'+' Predição de Consumo\n'+'\n'+' Altura de Onda: ' + str(selfori.altura_onda) + ' m\n Velocidade do Vento: ' + str(selfori.velocidade_vento) + ' m/s\n'+' Direção do Vento: ' + str(selfori.direcao_vento) + '°\n Temperatura Ambiente: ' + str(selfori.temperatura_ambiente) + '°C\n'+' Velocidade de Serviço: ' + str(selfori.velocidade) + ' nós\n'+' Potência do Motor 1: ' + str(selfori.potencia1) + ' kW\n'+' Rotação do Motor 1: ' + str(selfori.rotacao1) + ' rpm\n'+' Potência do Motor 2: ' + str(selfori.potencia2) + ' kW\n'+' Rotação do Motor 2: ' + str(selfori.rotacao2) + ' rpm')

        with open('Relatório.txt','a',encoding = 'utf-8') as relatorio:
            relatorio.write('\n'+'\n Predição de Consumo total: ' + str(previsao[0][0]) + ' g/h\n'+' Predição de consumo para cada motor: ' + str(round((previsao[0][0])/2,2)) + ' kW')

    def predicao_de_velocidade(self,selfori,treino):
        if treino:

            r=messagebox.askyesno(title='Atenção',message='''
Você selecionou a opção de treinamento, esse processo
pode demorar muitas horas ou até dias, dependendo do seu 
banco de dados.

Deseja continuar?''')
            print(r)
            if not r:
                treino=False
            else:
                treino=True
  # Carregando os dados de predição a partir da planilha gerada anteriormente
            # Fazendo previsões em novos dados
            # Salvando dados informados pelo usuário
        
            # Normalização das características (opcional, mas geralmente recomendada)


        selfori.altura_onda = float(selfori.caixaaltura_onda_predicao_velocidade.get())
        selfori.velocidade_vento = float(selfori.caixavelocidade_vento_predicao_velocidade.get())
        selfori.direcao_vento = float(selfori.caixadirecao_vento_predicao_velocidade.get())
        selfori.temperatura_ambiente = float(selfori.caixatemperatura_ambiente_predicao_velocidade.get())
        selfori.consumo = float(selfori.caixaconsumo_predicao_velocidade.get())
        selfori.potencia1 = float(selfori.caixapotencia1_predicao_velocidade.get())
        selfori.rotacao1 = float(selfori.caixarotacao1_predicao_velocidade.get())
        selfori.potencia2 = float(selfori.caixapotencia2_predicao_velocidade.get())
        selfori.rotacao2 = float(selfori.caixarotacao2_predicao_velocidade.get())
        novos_dados=[[
selfori.altura_onda ,
selfori.velocidade_vento ,
selfori.direcao_vento ,
selfori.temperatura_ambiente ,
selfori.consumo ,
selfori.potencia1 ,
selfori.rotacao1 ,
selfori.potencia2 ,
selfori.rotacao2 
        ]]

        # Transformando os dados fornecidos pelo usuário num dataframe que será usado para predição

        




        if treino:
            selfori.df_novo = pd.read_excel('Dados.xlsx')
            selfori.df_predicao = pd.DataFrame((selfori.df_novo.SIG_WAVE_HEIGHT_M_COR,
                                                selfori.df_novo.WIND_SPEED_M_PER_S_COR,
                                                selfori.df_novo.REL_WIND_DIRECTION,
                                                selfori.df_novo.TEMPERATURE_C,
                                                selfori.df_novo.E1_E2_CONSUMO_GH,
                                                selfori.df_novo.E1_POTÊNCIA_KW,
                                                selfori.df_novo.E1_ROTAÇÃO_RPM,
                                                selfori.df_novo.E2_POTÊNCIA_KW,
                                                selfori.df_novo.E2_ROTAÇÃO_RPM,
                                                selfori.df_novo.VESSEL_KNOTS),
                                                index=["SIG_WAVE_HEIGHT_M",
                                                       "WIND_SPEED_M_PER_S",
                                                       "WIND_DIRECTION",
                                                       "TEMPERATURE_C",
                                                       "E1_E2_CONSUMO_GH",
                                                       "E1_POTÊNCIA_KW",
                                                       "E1_ROTAÇÃO_RPM",
                                                       "E2_POTÊNCIA_KW",
                                                       "E2_ROTAÇÃO_RPM",
                                                       "VESSEL_KNOTS"]).T


            # Separando as características (X) e os valores de resposta (y)
            x = selfori.df_predicao.iloc[:, :-1].values  # Todas as colunas, exceto a última
            y = selfori.df_predicao.iloc[:, -1].values  # A última coluna

            # Dividindo os dados em conjuntos de treinamento e teste
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

            # Confloatuindo os modelos da rede neural
            model = tf.keras.Sequential([
                tf.keras.layers.Input(shape=(x_train.shape[1],)),  # Camada de entrada com o número de características
                tf.keras.layers.Dense(512, activation='relu'),  # Camada oculta com 512 neurônios e ativação ReLU
                tf.keras.layers.Dense(256, activation='relu'),  # Camada oculta com 256 neurônios e ativação ReLU
                tf.keras.layers.Dense(128, activation='relu'),  # Camada oculta com 128 neurônios e ativação ReLU
                tf.keras.layers.Dense(64, activation='relu'),  # Camada oculta com 64 neurônios e ativação ReLU
                tf.keras.layers.Dense(32, activation='relu'),  # Camada oculta com 32 neurônios e ativação ReLU
                tf.keras.layers.Dense(1)  # Camada de saída com 1 neurônio para regressão
            ])

            
            model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_absolute_error'])
            model.fit(x_train, y_train, epochs=100, batch_size=32, validation_data=(x_test, y_test))
            model.save('modelo_treinado_veloc.keras')


        else:
            try:
                model = load_model('modelo_treinado_veloc.keras')
            except:
                messagebox.showerror(title='ERRO',message='''
Não existe um modelo treinado para a predição.
Por favor, clique em [TREINAR] para treinar o modelo.''')
           

        previsao = model.predict(novos_dados)
        print(previsao)
        lblPredicaoVelocidade = Label(selfori.frame_predicao_de_velocidade,text = "PREDIÇÃO DE VELOCIDADE :" + str(previsao[0][0]) + " nós ")
        lblPredicaoVelocidade.place(x = 40,y = 285)

        with open('Relatório.txt','a',encoding = 'utf-8') as relatorio:
            relatorio.write('\n'+'\n'+'\n'+' Predição de velocidade\n'+'\n'+' Altura de Onda: ' + str(selfori.altura_onda) + ' m\n Velocidade do Vento: ' + str(selfori.velocidade_vento) + ' m/s\n'+' Direção do Vento: ' + str(selfori.direcao_vento) + '°\n Temperatura Ambiente: ' + str(selfori.temperatura_ambiente) + '°C\n'+' Consumo : ' + str(selfori.consumo) + ' nós\n'+' Potência do Motor 1: ' + str(selfori.potencia1) + ' kW\n'+' Rotação do Motor 1: ' + str(selfori.rotacao1) + ' rpm\n'+' Potência do Motor 2: ' + str(selfori.potencia2) + ' kW\n'+' Rotação do Motor 2: ' + str(selfori.rotacao2) + ' rpm')

        with open('Relatório.txt','a',encoding = 'utf-8') as relatorio:
            relatorio.write('\n'+'\n Predição de velocidade total: ' + str(previsao[0][0]) + ' nós\n'+' Predição de velocidade para cada motor: ' + str(round((previsao[0][0])/2,2)) + ' kW')










'''

class teste:
     def __init__(self) :
          dados=[[1,1,1,1,1,1,1,1,1]]
          rede(dados).predicao_de_consumo(self)
     
     
teste()
#oi=rede()
#oi.treinar()
'''