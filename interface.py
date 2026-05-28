import tkinter as tk

from database import *

#cria tabela
criar_tabela()

#-----------------------
#JANELA
#-----------------------

janela= tk.Tk()

janela.title("Sistema de Alunos")

janela.geometry("700x500")

#-----------------------------
#TÍTULO
#----------------------------

titulo = tk.Label(
    janela,
    text="cadastro de Alunos",
    font=("Arial", 20)
)

titulo.pack(pady=20)

#-------------------------
#NOME
#------------------------

label_nome = tk.Label(
    janela,
    text="Nome"
)

label_nome.pack()

campo_nome = tk.Entry(
    janela,
    width=40
)

campo_nome.pack()

#-----------------------
#EMAIL
#----------------------

label_email = tk.Label(
    janela,
    text="Email"
)

label_email.pack()

campo_email = tk.Entry(
    janela,
    width=40
)

campo_email.pack()

#---------------------
#CURSO
#--------------------

label_curso = tk.Label(
    janela,
    text="curso"
)

label_curso.pack()

campo_curso = tk.Entry(
    janela,
    width=40
)

campo_curso.pack()

#----------------------
#LISTA
#----------------------

lista = tk.Listbox(
    janela,
    width=100
)

lista.pack(pady=20)

#-------------------
#FUNÇÃO CADASTRAR
#------------------

def cadastrar():
    nome= campo_nome.get()
    email= campo_email.get()
    curso = campo_curso.get()
    inserir_aluno(nome, email, curso)
    print("Aluno cadastrado!")

 #--------------------------
 # FUNÇÃO LISTAR
 #--------------------------


def listar():

    lista.delete(0, tk.END)

    alunos = listar_alunos()

    for aluno in alunos:

        texto = f"ID: {aluno[0]} | Nome: {aluno[1]} | Email: {aluno[2]} | Curso: {aluno[3]}"

        lista.insert(tk.END, texto)

#---------------------------
#BOTÃO CADASTRAR
#--------------------------

botao_cadastrar = tk.Button(
    janela,
    text="Cadastrar",
    command=cadastrar
)

botao_cadastrar.pack(pady=10)

#----------------------------
#BOTÃO LISTAR
#---------------------------

botao_listar = tk.Button(
    janela,
    text="Listar Alunos",
    command=listar
)

botao_listar.pack(pady=10)

#--------------------------
#LOOP
#--------------------------

janela.mainloop()
 
