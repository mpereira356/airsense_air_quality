from tkinter import *
from tkinter.ttk import *

janela = Tk()
janela.title('Combobox')
janela.geometry('300x250')

# nome ----------------------
labe_nome = Label(janela, width=15, height=2, text='Faça a sua escolha',font=('Arial 10'), anchor='w')
label_nome.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)

combo = Combobox(janela)
combo['values'] = (1,2,3,4)

botao = Button(janela, width=10, height=1, text='Ver resposta', relief='raised', bg='white')
botao.grid(row=2, column=0, padx=5, pady=20)

janela.mainloop()
