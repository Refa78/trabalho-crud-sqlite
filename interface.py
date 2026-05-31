import tkinter as tk

from database import *

#cria tabela
criar_tabela()

#-----------------------
#JANELA
#-----------------------

janela= tk.Tk()
janela.title("Sistema de Alunos")
janela.geometry("1000x700")

#-----------------------------
#TÍTULO
#---------------------------

titulo = tk.Label(
    janela,
    text="Cadastro de Alunos",
    font=("Arial", 20)
)
titulo.pack(pady=20)

#-------------------------
# FRAME DAS ENTRADAS
#------------------------

frame_inputs = tk.Frame(janela)
frame_inputs.pack(pady=10)

#-------------------------
#NOME
#------------------------

label_nome = tk.Label(
    frame_inputs,
    text="Nome:"
)
label_nome.grid(
    row=0,
    column=0,
    padx=5, 
    pady=5, 
    sticky="e"
)

campo_nome = tk.Entry(
    frame_inputs,
    width=40
)

campo_nome.grid(
    row=0, 
    column=1, 
    padx=5, 
    pady=5
)

#-----------------------
#EMAIL
#----------------------

label_email = tk.Label(
    frame_inputs,
    text="Email:"
)

label_email.grid(
    row=1,
    column=0,
    padx=5,
    pady=5,
    sticky="e"
)

campo_email = tk.Entry(
    frame_inputs,
    width=40
)

campo_email.grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)

#---------------------
#CURSO
#--------------------

label_curso = tk.Label(
    frame_inputs,
    text="Curso:"
)

label_curso.grid(
    row=2,
    column=0,
    padx=5,
    pady=5,
    sticky="e"
)

campo_curso = tk.Entry(
    frame_inputs,
    width=40
)

campo_curso.grid(
    row=2,
    column=1,
    padx=5,
    pady=5
)

label_id = tk.Label(
    frame_inputs,
    text="ID:"
)

label_id.grid(
    row=3,
    column=0,
    padx=5,
    pady=5,
    sticky="e"
)

campo_id = tk.Entry(
    frame_inputs,
    width=40
)

campo_id.grid(
    row=3,
    column=1,
    padx=5,
    pady=5
)

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
    lista.delete(0, tk.END)
    lista.insert(tk.END, "Aluno cadastrado com sucesso!")

 #--------------------------
 # FUNÇÃO LISTAR
 #--------------------------


def listar():

    lista.delete(0, tk.END)
    alunos = listar_alunos()
    
    for aluno in alunos:
        texto = f"ID: {aluno[0]} | Nome: {aluno[1]} | Email: {aluno[2]} | Curso: {aluno[3]}"
        lista.insert(tk.END, texto)

def buscar():
    id_aluno = campo_id.get()
    aluno = buscar_aluno_por_id(id_aluno)

    if aluno:
        texto = f"ID: {aluno[0]} | Nome: {aluno[1]} | Email: {aluno[2]} | Curso: {aluno[3]}"
        lista.delete(0, tk.END)
        lista.insert(tk.END, texto)
    else:
        lista.delete(0, tk.END)
        lista.insert(tk.END, "Aluno não encontrado.")

 #--------------------------
 # FUNÇÃO ATUALIZAR
 #--------------------------

def atualizar():
    id_aluno = campo_id.get()
    aluno = buscar_aluno_por_id(id_aluno)

    if aluno:
        nome = campo_nome.get()
        email = campo_email.get()
        curso = campo_curso.get()

        atualizar_aluno(id_aluno, nome, email, curso)
        lista.delete(0, tk.END)
        lista.insert(tk.END, "Aluno atualizado com sucesso!")
    else:
        lista.delete(0, tk.END)
        lista.insert(tk.END, "Aluno não encontrado.")

#--------------------------
# FUNÇÃO EXCLUIR
#--------------------------

def deletar():
    id_aluno = campo_id.get()
    deletar_aluno(id_aluno)
    lista.delete(0, tk.END)
    lista.insert(tk.END, "Aluno deletado com sucesso!")

#---------------------------
# FRAME DOS BOTÕES
#--------------------------

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=20, anchor=tk.CENTER)

#---------------------------
#BOTÃO CADASTRAR
#--------------------------

botao_cadastrar = tk.Button(
    frame_botoes,
    text="Cadastrar",
    command=cadastrar
)

botao_cadastrar.pack(side=tk.LEFT, padx=10)

#----------------------------
#BOTÃO LISTAR
#---------------------------

botao_listar = tk.Button(
    frame_botoes,
    text="Listar Alunos",
    command=listar
)

botao_listar.pack(side=tk.LEFT, padx=10)

 #--------------------------
 # BOTÃO BUSCAR
 #--------------------------

botao_buscar = tk.Button(
    frame_botoes,
    text="Buscar",
    command=buscar
)

botao_buscar.pack(side=tk.LEFT, padx=10)


#--------------------------
# BOTÃO ATUALIZAR
#--------------------------

botao_atualizar = tk.Button(
    frame_botoes,
    text="Atualizar",
    command=atualizar
)
botao_atualizar.pack(side=tk.LEFT, padx=10)

 #--------------------------
 # BOTÃO EXCLUIR
 #--------------------------

botao_excluir = tk.Button(
    frame_botoes,
    text="Excluir",
    command=deletar
)

botao_excluir.pack(side=tk.LEFT, padx=10)

#--------------------------
#LOOP
#--------------------------

janela.mainloop()