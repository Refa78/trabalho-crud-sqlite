import sqlite3

def conectar():
    return sqlite3.connect("sistema.db")

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            curso TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()

def inserir_aluno(nome, email, curso):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO alunos (nome, email, curso)
        VALUES (?, ?, ?)
    """, (nome, email, curso))

    conexao.commit()
    conexao.close()

def listar_alunos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM alunos")
    alunos = cursor.fetchall()

    conexao.close()
    return alunos

def buscar_aluno_por_id(id_aluno):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM alunos WHERE id = ?", (id_aluno,))
    aluno = cursor.fetchone()

    conexao.close()
    return aluno

def atualizar_aluno(id_aluno,nome, email, curso):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE alunos
        SET nome = ?, email = ?, curso = ?
        WHERE id = ?
    """, (nome, email, curso, id_aluno))

    conexao.commit()
    conexao.close()

def deletar_aluno(id_aluno):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM alunos WHERE id = ?", (id_aluno,))

    conexao.commit()
    conexao.close()