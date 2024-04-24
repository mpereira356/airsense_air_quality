from tkinter import Tk
from tkinter import *
from tkinter import Tk, ttk, Button, Toplevel, Label, Entry
from tkinter import messagebox
import locale
from twilio.rest import Client

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

# importando funcoes da view

# cores
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

colors = ['#5588bb', '#66bbbb','#99bb55', '#ee9944', '#444466', '#bb5555']


# criando janela====================
janela = Tk()
janela.title("AirSense")
janela.geometry('900x650')
janela.configure(background=co2)  
janela.resizable(width=FALSE, height=FALSE)

# criando frames=========================
frameCima = Frame(janela, width=1043, height=50, bg=co1, relief="flat")
frameCima.grid(row=0, column=0)

frameMeio = Frame(janela, width=1043, height=661, bg=co1, pady=20, relief="raised")
frameMeio.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

# Frame Cima=======================
# acessando a imagem
app_img = Image.open('logo.png')
app_img = app_img.resize((45, 45))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frameCima, image=app_img, text="Monitoramento de Qualidade do Ar", width=900, compound=LEFT, padx=5, relief=RAISED,
                 anchor=NW, font=('Verdana 20 bold'), bg=co1, fg=co4,)
app_logo.place(x=0, y=0)

# Dicionário para mapear nomes de cidades aos IDs correspondentes
cidades_ids = {'Perus': "@12576", 'Guarulhos': "@343", 'Araçatuba': "@330",
    'Araraquara': "@331",
    'Bauru': "@332",
    'Campinas-Centro': "@333",
    'Capão Redondo': "@334",
    'Carapicuíba': "@335",
    'Catanduva': "@336",
    'Cerqueira César': "@337",
    'Congonhas': "@338",
    'Cubatão-Centro': "@339",
    'Itaquera':"@330",
    'Bairro-Alto': "A361210"} #bairro alto é de minas gerais


# Função para atualizar a URL com base na seleção do usuáario
def atualizar_url():
    cidade_selecionada = combo_categoria_cidade.get()
    cidade_id = cidades_ids.get(cidade_selecionada, "here")  # Valor padrão é "@12576" se não houver correspondência
    url = f"https://api.waqi.info/feed/{cidade_id}/?token=58de93499ccd776cae6c54fdbae1f4b43868d886"
    
    # Obter os valores atmosféricos
    obt_pm25, obt_pm10, obt_o3 = obter_valores_atmosfericos()
    # Atualizar o gráfico de barras
    grafico_bar()
    # Chamar as funções
    resumo(obt_pm25, obt_pm10, obt_o3)
    percentagem(obt_pm25, obt_pm10, obt_o3)  # Passar os valores para a função percentagem
    print("URL atualizada:", url)
    print("Valor de PM2.5:", obt_pm25)
    print("Valor de PM10:", obt_pm10)
    print("Valor de O3:", obt_o3)


cidades_por_estado = {
    'São Paulo': ['Perus', 'Guarulhos', 'Araçatuba', 'Araraquara', 'Bauru', 'Campinas-Centro', 'Capão Redondo', 'Carapicuíba', 'Catanduva', 'Cerqueira César', 'Congonhas', 'Cubatão-Centro', 'Itaquera'],
    'Minas Gerais': ['Bairro-Alto']
}
# Função para atualizar as cidades com base no estado selecionado
def atualizar_cidades():
    estado_selecionado = combo_categoria_estado.get()
    cidades_estado = cidades_por_estado.get(estado_selecionado, [])
    combo_categoria_cidade['values'] = cidades_estado
    combo_categoria_cidade.current(0)  # Selecionar a primeira cidade por padrão
    atualizar_url()

#COMBO BOX
# Combobox de seleção de estado
combo_categoria_estado = ttk.Combobox(frameMeio, width=13, font=('Ivy 10'))
combo_categoria_estado['values'] = list(cidades_por_estado.keys())  # nomes dos estados como valores do combobox
combo_categoria_estado.place(x=65, y=41)
combo_categoria_estado.bind("<<ComboboxSelected>>", lambda event: atualizar_cidades())

# Combobox de seleção de cidade
combo_categoria_cidade = ttk.Combobox(frameMeio, width=13, font=('Ivy 10'))
combo_categoria_cidade.place(x=235, y=41)
combo_categoria_cidade.bind("<<ComboboxSelected>>", lambda event: atualizar_url())


l_estado = Label(frameMeio, text='Estado', height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_estado.place(x=10, y=40)

l_cidade = Label(frameMeio, text='Cidade', height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_cidade.place(x=180, y=40)

l_notificar = Label(frameMeio, text='Notificar as previsões:', height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_notificar.place(x=85, y=470)

# Função para obter o valor de PM2.5 com base na cidade selecionada
def obter_valores_atmosfericos():
    global url
    cidade_selecionada = combo_categoria_cidade.get()
    cidade_id = cidades_ids.get(cidade_selecionada, "here")  # Valor padrão começa como ip do usuário para encontrar localidade.
    url = f"https://api.waqi.info/feed/{cidade_id}/?token=58de93499ccd776cae6c54fdbae1f4b43868d886"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pm25_value = data['data']['iaqi'].get('pm25', {}).get('v', None)
        pm10_value = data['data']['iaqi'].get('pm10', {}).get('v', None)
        o3_value = data['data']['iaqi'].get('o3', {}).get('v', None)
        return pm25_value, pm10_value, o3_value
    else:
        print("Falha ao obter dados da API")
        return None, None, None


def obter_nomecity():
    cidade_selecionada = combo_categoria_cidade.get()
    cidade_id = cidades_ids.get(cidade_selecionada, "here")  # Valor padrão começa como ip do usuario para encontrar localidade.
    url = f"https://api.waqi.info/feed/{cidade_id}/?token=58de93499ccd776cae6c54fdbae1f4b43868d886"
    # Fazendo a solicitação HTTP GET
    response = requests.get(url)

    # Verificando se a solicitação foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        # Analisando a resposta JSON
        data = response.json()
        # Obtendo o nome da cidade
        nome_cidade = data['data']['city']['name']
        return nome_cidade 
    else:
        print("Falha ao obter dados da API")
        return None
    



#data atual===========================
data_atual = datetime.today()
# data limite (7 dias a partir de hoje)-------------*****
data_limite = data_atual + timedelta(days=7)

# data ---------------------
# seleção de data

l_data = Label(frameMeio, text='Data', height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_data.place(x=350, y=40)

e_cal_data = DateEntry(frameMeio, width=12, background='darkblue', foreground='white', borderwidth=2, year=data_atual.year, month=data_atual.month, day=data_atual.day, date_pattern='dd/mm/yyyy')


# Definindo a posição do widget
e_cal_data.place(x=390, y=41)

# Obtendo a data atual
data_atual = datetime.today()

# Calculando a data limite (7 dias a partir de hoje)
data_limite = data_atual + timedelta(days=7)

# Definindo a data mínima e máxima permitida para seleção
e_cal_data.config(mindate=data_atual, maxdate=data_limite)

# BOTÃO Pesquisar------------------
img_add_src = Image.open('src.png')
img_add_src = img_add_src.resize((17, 17))
img_add_src = ImageTk.PhotoImage(img_add_src)
botao_inserir_src = Button(frameMeio, image=img_add_src, text="Pesquisar".upper(), width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=RIDGE)
botao_inserir_src.place(x=500, y=38)

# BOTÃO PM2.5------------------
img_add_pm25 = Image.open('add.png')
img_add_pm25 = img_add_pm25.resize((17, 17))
img_add_pm25 = ImageTk.PhotoImage(img_add_pm25)
botao_inserir_pm25 = Button(frameMeio, image=img_add_pm25, text="PM 2.5".upper(), width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=RIDGE)
botao_inserir_pm25.place(x=560, y=525)

# BOTÃO O2-----------------------------
img_add_o3 = Image.open('o3.png')
img_add_o3 = img_add_o3.resize((17, 17))
img_add_o3 = ImageTk.PhotoImage(img_add_o3)
botao_inserir_o2 = Button(frameMeio, image=img_add_o3, text="O3".upper(), width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=RIDGE)
botao_inserir_o2.place(x=670, y=525)

# BOTÃO pm10-------------------------
img_add_pm10 = Image.open('add.png')
img_add_pm10 = img_add_pm10.resize((17, 17))
img_add_pm10 = ImageTk.PhotoImage(img_add_pm10)
botao_inserir_pm10 = Button(frameMeio, image=img_add_pm10, text="pm10".upper(), width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=RIDGE)
botao_inserir_pm10.place(x=780, y=525)



# Função para abrir a janela de informações-----------
def abrir_legenda():
    # Criando uma nova janela (top-level window)-------------
    legenda_window = Toplevel(janela)
    legenda_window.title("Legenda")
    legenda_window.geometry("650x220")

    # Adicionando um rótulo com as informações------
    legenda_label = Label(legenda_window, text="Legenda:", font=('Verdana 12 bold'))
    legenda_label.pack()

    # Informações sobre PM 2.5-------------
    pm25_label = Label(legenda_window, text="  - PM 2.5: Partículas finas no ar com diâmetro menor que 2.5 micrômetros.", font=('Verdana 10'))
    pm25_label.pack(anchor='w')

    # Informaçoes sobre o3--------
    o3_label = Label(legenda_window, text="  - O3: Ozônio, gás prejudicial à saúde em altas concentrações.", font=('Verdana 10'))
    o3_label.pack(anchor='w')

    # Informações sobre PM10---------
    pm10_label = Label(legenda_window, text="  - PM10: Partículas no ar com diâmetro menor que 10 micrômetros.", font=('Verdana 10'))
    pm10_label.pack(anchor='w')

    # Informações sobre umidade===
    umidade_label = Label(legenda_window, text="  - h:   Umidade: Quantidade de vapor de água na atmosfera em relação à máxima possível.", font=('Verdana 10'))
    umidade_label.pack(anchor='w')

    #Informações sobre pressão atmosférica -----=
    pressao_label = Label(legenda_window, text="  - p:   Pressão Atmosférica: Força exercida pela massa de ar sobre um ponto na Terra.", font=('Verdana 10'))
    pressao_label.pack(anchor='w')

    # Informações sobre temperatura--------------
    temperatura_label = Label(legenda_window, text="  - t:    Temperatura: Quantidade de calor presente na atmosfera em um local e momento.", font=('Verdana 10'))
    temperatura_label.pack(anchor='w')

    # Informações sobre velocidade do vento-----------
    vento_label = Label(legenda_window, text="  - w:   Velocidade do Vento: Medida da movimentação do ar em relação à superfície terrestre.", font=('Verdana 10'))
    vento_label.pack(anchor='w')

    #Informções sobre rajadas de vento-----------
    rajadas_vento_label = Label(legenda_window, text="  - wg:    Rajadas de Vento: Variações temporárias e repentinas na velocidade do vento.", font=('Verdana 10'))
    rajadas_vento_label.pack(anchor='w')

    


# BOTÃO legenda==================
img_add_leg = Image.open('info.png')
img_add_leg = img_add_leg.resize((17, 17))
img_add_leg = ImageTk.PhotoImage(img_add_leg)
botao_inserir_leg = Button(frameMeio, image=img_add_leg, text="  Legenda".upper(), width=80, compound="left", anchor="nw", font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief="ridge", command=abrir_legenda)
botao_inserir_leg.place(x=800, y=20)


####################           ##########         ##########################

def grafico_bar():
    global pm25_values, pm10_values, o3_values

    cidade_selecionada = combo_categoria_cidade.get()
    cidade_id = cidades_ids.get(cidade_selecionada, "here") 
    url = f"https://api.waqi.info/feed/{cidade_id}/?token=58de93499ccd776cae6c54fdbae1f4b43868d886"
    response = requests.get(url)
    if response.status_code != 200:
        print("Falha ao obter dados do JSON")
        return

    # Inicializar a lista de dias
    days = []

    try:
        # Tentar extrair os valores do forecast do JSON
        forecast_data = response.json()["data"]["forecast"]["daily"]
    except KeyError:
        # Se a chave 'forecast' não existir, definir todos os valores como 0
        print("Sem previsão para essa cidade")
        pm25_values = [0] * len(days)
        pm10_values = [0] * len(days)
        o3_values = [0] * len(days)
    else:
        # Se a chave 'forecast' existir, extrair os valores normalmente
        pm25_values = [day["avg"] if day is not None else 0 for day in forecast_data.get("pm25", [])]
        pm10_values = [day["avg"] if day is not None else 0 for day in forecast_data.get("pm10", [])]
        o3_values = [day["avg"] if day is not None else 0 for day in forecast_data.get("o3", [])]
        days = [day["day"] for day in forecast_data.get("pm25", [])]  

    # Criar o gráfico de barras com o tamanho e dpi desejados
    figura, ax = plt.subplots(figsize=(6, 6.45), dpi=60)
    bar_width = 0.25
    index = range(len(days))
    ax.bar(index, pm25_values, bar_width, label='PM 2.5', color='b')
    ax.bar([i + bar_width for i in index], pm10_values, bar_width, label='PM 10', color='g')
    ax.bar([i + bar_width*2 for i in index], o3_values, bar_width, label='O3', color='r')

    ax.set_xlabel('Dias')
    ax.set_ylabel('Valores')
    ax.set_title('Valores dos poluentes atmosféricos')
    ax.set_xticks([i + bar_width for i in index])
    ax.set_xticklabels(days, rotation=45)
    ax.legend()

    # Adicionar o gráfico ao seu aplicativo Tkinter existente
    canvas = FigureCanvasTkAgg(figura, master=frameMeio)
    canvas.draw()
    canvas.get_tk_widget().place(x=520, y=120)



# Declarar as variáveis globais fora de qualquer função
# Definir variáveis globais
l_nome = None
qualidade = None
text_bar = None
canvas = None

# Função percentagem
def percentagem(obt_pm25, obt_pm10, obt_o3):
    global l_nome, qualidade, text_bar, canvas  # Adicionar declarações globais aqui

    # Verificar se o rótulo l_nome já existe e destruí-lo, se sim
    if l_nome:
        l_nome.destroy()
    
    # Verificar se o rótulo qualidade já existe e destruí-lo, se sim
    if qualidade:
        qualidade.destroy()

    # Verificar se o rótulo text_bar já existe e destruí-lo, se sim
    if text_bar:
        text_bar.destroy()

    # Definindo os intervalos e as cores correspondentes
    bar = Progressbar(frameMeio, length=180, style='black.Horizontal.TProgressbar', maximum=500)
    bar.place(x=30, y=132)
    bar['value'] = obt_pm25 or obt_pm10 or obt_o3
    valor = obt_pm25 or obt_pm10 or obt_o3

    # Informação da qualidade
    if valor >= 0 and valor <= 50:
        qualidade_texto = 'Boa'  
    elif valor >= 51 and valor <= 100:
        qualidade_texto = 'Moderada'  
    elif valor >= 101 and valor <= 150:
        qualidade_texto = 'Não saudável para grupos sensíveis'  
    elif valor >= 151 and valor <= 200:
        qualidade_texto = 'Pouco saudável'  
    elif valor >= 201 and valor <= 300:
        qualidade_texto = 'Muito prejudicial à saúde'  
    elif valor >= 301 and valor <= 500:
        qualidade_texto = 'Perigoso!'  
    else:
        qualidade_texto = 'Sem valor'  

    # Obtendo o nome da cidade
    nome_city = obter_nomecity()

    l_nome = Label(frameMeio, text=f"Região selecionada: {nome_city}, a qualidade do ar \n atualmente está {valor} ", height=2, anchor=NW, font=('Verdana 12 bold' ), bg=co1, fg=co4)
    l_nome.place(x=27, y=80)

    # Cor da barra de acordo com qualidade
    if valor >= 0 and valor <= 50:
        cor_barra = '#00FF00'  # Verde
    elif valor >= 51 and valor <= 100:
        cor_barra = '#FFFF00'  # Amarelo
    elif valor >= 101 and valor <= 150:
        cor_barra = '#FFA500'  # Laranja
    elif valor >= 151 and valor <= 200:
        cor_barra = '#FFD700'  # Vermelho claro
    elif valor >= 201 and valor <= 300:
        cor_barra = '#800080'  # Roxo
    elif valor >= 301 and valor <= 500:
        cor_barra = '#8B0000'  # Vermelho escuro
    else:
        cor_barra = '#000000'  # Cor padrão (preto) para outros valores

    style = ttk.Style()
    style.theme_use('default')
    style.configure("black.Horizontal.TProgressbar", background=cor_barra)
    style.configure("TProgressbar", thickness=25)
    text_bar = Label(frameMeio, text=qualidade_texto, font=('Verdana', 10))
    text_bar.place(x=220, y=132, anchor="w")

    # Armazenar o rótulo qualidade_texto como uma variável global
    qualidade = text_bar


    


# Definir variáveis globais
l_sumario_pm25 = None
l_sumario_pm10 = None
l_sumario_o3 = None

# Função resumo
def resumo(obt_pm25, obt_pm10, obt_o3):
    global l_sumario_pm25, l_sumario_pm10, l_sumario_o3  # Adicione declarações globais aqui

    # Destruir os rótulos existentes, se existirem
    if l_sumario_pm25:
        l_sumario_pm25.destroy()
    if l_sumario_pm10:
        l_sumario_pm10.destroy()
    if l_sumario_o3:
        l_sumario_o3.destroy()

    # Exibicao valores
    l_nome = Label(frameMeio, text="Poluentes atmosféricos atuais na região:", height=1, anchor=NW, font=('Verdana 12 bold' ), bg=co1, fg=co4)
    l_nome.place(x=25, y=200)
    
    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=30, y=252)

    # Verificar se obt_pm25 é None
    if obt_pm25 is not None:
        l_sumario_pm25 = Label(frameMeio, text="PM 2.5                                 ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg="#83a9e6")
        l_sumario_pm25.place(x=30, y=235)
        l_sumario_pm25_valor = Label(frameMeio, text=obt_pm25, anchor=NW, font=('Arial 17'), bg=co1, fg="#545454")
        l_sumario_pm25_valor.place(x=30, y=270)
    else:
        l_sumario_pm25 = Label(frameMeio, text="PM 2.5                                 ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg="#83a9e6")
        l_sumario_pm25.place(x=30, y=235)
        l_sumario_pm25_valor = Label(frameMeio, text="Sem valor", anchor=NW, font=('Arial 17'), bg=co1, fg="#545454")
        l_sumario_pm25_valor.place(x=30, y=270)

    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=30, y=332)

    # Verificar se obt_pm10 é None
    if obt_pm10 is not None:
        l_sumario_pm10 = Label(frameMeio, text="PM 10                                     ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg="#83a9e6")
        l_sumario_pm10.place(x=30, y=315)
        l_sumario_pm10_valor = Label(frameMeio, text=obt_pm10, anchor=NW, font=('Arial 17'), bg=co1, fg="#545454")
        l_sumario_pm10_valor.place(x=30, y=350)
    else:
        l_sumario_pm10 = Label(frameMeio, text="PM 10                                     ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg="#83a9e6")
        l_sumario_pm10.place(x=30, y=315)
        l_sumario_pm10_valor = Label(frameMeio, text="Sem valor", anchor=NW, font=('Arial 17'), bg=co1, fg="#545454")
        l_sumario_pm10_valor.place(x=30, y=350)

    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=30, y=407)

    # Verificar se obt_o3 é None
    if obt_o3 is not None:
        l_sumario_o3 = Label(frameMeio, text="O3                                      ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg="#83a9e6")
        l_sumario_o3.place(x=30, y=390)
        l_sumario_o3_valor = Label(frameMeio, text=obt_o3, anchor=NW, font=('Arial 17'), bg=co1, fg="#545454")
        l_sumario_o3_valor.place(x=30, y=420)
    else:
        l_sumario_o3 = Label(frameMeio, text="O3                                      ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg="#83a9e6")
        l_sumario_o3.place(x=30, y=390)
        l_sumario_o3_valor = Label(frameMeio, text="Sem valor", anchor=NW, font=('Arial 17'), bg=co1, fg="#545454")
        l_sumario_o3_valor.place(x=30, y=420)

    # Atribuir os novos rótulos às variáveis globais
    l_sumario_pm25 = l_sumario_pm25_valor
    l_sumario_pm10 = l_sumario_pm10_valor
    l_sumario_o3 = l_sumario_o3_valor


# NOTIFICAR SMS
def enviar_sms(dias_selecionados):
    numero_destino = entry_numero.get()
    if numero_destino:
        # Configuração da conta Twilio
        account_sid = #'ID DO TWILIO'
        auth_token = #'TOKEN TWILIO'
        twilio_number = #'TWILIO NUMERO'
        
        # Inicializar o cliente Twilio
        client = Client(account_sid, auth_token)
        
        # Mensagem a ser enviada
        mensagem = ""

        # Iterar sobre os dias selecionados
        for data_correspondente in dias_selecionados:
            # Obter o índice do dia selecionado em relação ao dia de hoje
            indice = (data_correspondente - datetime.now().date()).days

            # Verificar se o índice está dentro do intervalo de dias disponíveis
            if 0 <= indice <= 6:
                try:
                    # Adicionar à mensagem a data e os valores de PM2.5, PM10 e O3 correspondentes
                    valor_pm25 = pm25_values[indice]
                    valor_pm10 = pm10_values[indice]
                    valor_o3 = o3_values[indice]
                    mensagem += f"Previsões para a cidade: {nome_city} \n Dia {data_correspondente.strftime('%Y-%m-%d')}: PM2.5 = {valor_pm25},\n Dia {data_correspondente.strftime('%Y-%m-%d')}:PM10 = {valor_pm10}, Dia {data_correspondente.strftime('%Y-%m-%d')}: O3 = {valor_o3}\n"
                except IndexError:
                    # Tratar o erro de índice fora do intervalo
                    mensagem += f"Dia {data_correspondente.strftime('%Y-%m-%d')}: Sem previsão para essa cidade\n"
            else:
                mensagem += f"Dia {data_correspondente.strftime('%Y-%m-%d')}: Sem previsão para essa cidade\n"

        # Enviar mensagem
        try:
            client.messages.create(
                body=mensagem,
                from_=twilio_number,
                to=numero_destino
            )
            messagebox.showinfo("Sucesso", "SMS enviado com sucesso!")
        except Exception as e:
            # Tratar o erro ao enviar SMS
            messagebox.showerror("Erro", f"Erro ao enviar SMS: {str(e)}")
    else:
        messagebox.showerror("Erro", "Por favor, insira um número de telefone.")



# Função para abrir a janela com calendário integrado
def adicionar_dia_tabela(cal):
    dia_selecionado = cal.selection_get()
    if dia_selecionado not in dias_selecionados:
        dias_selecionados.append(dia_selecionado)
        id = tabela.insert('', 'end', values=(dia_selecionado.strftime('%Y-%m-%d'),))
        # Associar o identificador único com o objeto datetime correspondente
        tabela.item(id, values=(dia_selecionado.strftime('%Y-%m-%d'), dia_selecionado))
    else:
        messagebox.showerror("Erro", f"Dia {dia_selecionado.strftime('%Y-%m-%d')} já foi selecionado!")

def remover_dia_tabela():
    global dias_selecionados  # Adicionando a declaração global
    selection = tabela.selection()
    if selection:
        for item_id in selection:
            item = tabela.item(item_id)
            dia = item['values'][0]  # Obtendo a data como string da tabela
            print("Dia na tabela:", dia)
            print("Dias selecionados:", [d.strftime('%Y-%m-%d') for d in dias_selecionados])
            if dia in [d.strftime('%Y-%m-%d') for d in dias_selecionados]:
                # Encontramos a data na lista, então removemos da lista e da tabela
                dias_selecionados = [d for d in dias_selecionados if d.strftime('%Y-%m-%d') != dia]
                tabela.delete(item_id)
                messagebox.showinfo("Sucesso", f"Dia {dia} removido!")
            else:
                messagebox.showerror("Erro", f"Dia {dia} não está na lista!")

def abrir_janela():
    janela = Tk()
    janela.title("Enviar SMS")
    
    Label(janela, text="Número de Telefone:").pack()
    global entry_numero
    # Pré-preencher o campo de entrada com o prefixo internacional +55
    entry_numero = Entry(janela)
    entry_numero.insert(0, "+55")
    entry_numero.pack()
    
    data_inicial = datetime.now() - timedelta(days=2)
    data_final = datetime.now() + timedelta(days=4)
    cal = Calendar(janela, selectmode="day", mindate=data_inicial, maxdate=data_final)
    cal.pack(pady=20)

    btn_adicionar = Button(janela, text="Adicionar Dia", command=lambda: adicionar_dia_tabela(cal))
    btn_adicionar.pack()

    btn_remover = Button(janela, text="Remover Dia", command=remover_dia_tabela)
    btn_remover.pack()

    global tabela
    tabela = ttk.Treeview(janela, columns=('Dia',), show='headings')
    tabela.heading('Dia', text='Dia')
    tabela.pack(pady=20)

    global dias_selecionados
    dias_selecionados = []

    btn_enviar = Button(janela, text="Enviar SMS", command=lambda: enviar_sms(dias_selecionados))
    btn_enviar.pack()
    
    janela.mainloop()



    # BOTÃO notificar
img_notififcar = Image.open('notify.png')
img_notififcar= img_notififcar.resize((17, 17))
img_notififcar= ImageTk.PhotoImage(img_notififcar)
botao_notififcar = Button(frameMeio, image=img_notififcar, text="            NOTIFICAR".upper(), width=150, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=RIDGE, command=abrir_janela)
botao_notififcar.place(x=80, y=510)

# Obter os valores de PM2.5, PM10 e O3
obt_pm25, obt_pm10, obt_o3 = obter_valores_atmosfericos()
nome_city = obter_nomecity()

# Chamando as funções
percentagem(obt_pm25, obt_pm10, obt_o3)
grafico_bar()
resumo(obt_pm25, obt_pm10, obt_o3)

# Loop principal
janela.mainloop()