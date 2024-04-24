from tkinter import Tk
from tkinter import *
from tkinter import Tk, ttk, Button, Toplevel, Label
from tkinter import messagebox
import locale

import requests



#importanto Pillow
from PIL import Image, ImageTk

# importando barra de progresso
from tkinter.ttk import Progressbar

# importando Matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


# tkcalendar 
from tkcalendar import Calendar, DateEntry
from datetime import date
from datetime import datetime, timedelta


# Configurando o locale para português do Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.utf-8')

# importando Pillow
from PIL import Image, ImageTk


co0 = "#2e2d2b"  # Preta
co1 = "#feffff"  # branca
co2 = "#4fa882"  # verde
co3 = "#38576b"  # valor
co4 = "#403d3d"  # letra
co5 = "#e06636"  # - profit
co6 = "#038cfc"  # azul
co7 = "#3fbfb9"  # verde
co8 = "#263238"  # + verde
co9 = "#e9edf5"  # + verde

# Função para atualizar a URL da cidade selecionada
def atualizar_url_cidade(event=None):
    cidade_selecionada = combo_categoria_cidade.get()
    url_atualizada = f"https://api.waqi.info/feed/{cidade_selecionada}/?token=58de93499ccd776cae6c54fdbae1f4b43868d886"
    print("URL atualizada:", url_atualizada)

# Lista de cidades disponíveis
cidades_disponiveis = ["New York", "Los Angeles", "London", "Paris", "Tokyo"]

# Criando uma nova janela
janela = Tk()
janela.title("AirSense")
janela.geometry('400x200')

# Criando uma nova janela para os widgets
janela_widgets = Toplevel(janela)
janela_widgets.title("Selecionar Cidade")
janela_widgets.geometry('300x150')

# Combo box para selecionar a cidade
combo_categoria_cidade = Combobox(janela_widgets, width=13, font=('Ivy 10'))
combo_categoria_cidade['values'] = cidades_disponiveis
combo_categoria_cidade.place(x=50, y=50)
combo_categoria_cidade.bind("<<ComboboxSelected>>", atualizar_url_cidade)  # Associando a função ao evento de seleção

# criando frames=========================
frameCima = Frame(janela, width=1043, height=50, bg=co1, relief="flat")
frameCima.grid(row=0, column=0)

frameMeio = Frame(janela, width=1043, height=661, bg=co1, pady=20, relief="raised")
frameMeio.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

# Acessando o valor de 'pm25'
valor_pm25 = dados_json["data"]["iaqi"]["pm25"]["v"]

def resumo():

    # Exibicao valores
    l_nome = Label(frameMeio, text="Poluentes atmosféricos atuais na região:", height=1, anchor=NW, font=('Verdana 12 bold' ), bg=co1, fg=co4)
    l_nome.place(x=25, y=200)
    
    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=30, y=252)
    l_sumario = Label(frameMeio, text="PM 2.5                                 ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg="#83a9e6")
    l_sumario.place(x=30, y=235)
    l_sumario = Label(frameMeio, text=valor_pm25, anchor=NW, font=('Arial 17'), bg=co1, fg="#545454")
    l_sumario.place(x=30, y=270)

janela.mainloop()


