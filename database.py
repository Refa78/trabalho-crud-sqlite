import sqlite3

def conectar():
    return sqlite3.connect("sistema.db")

def criar_tabela():

    conexao = conectar()  #trocar funcao para (config_database())
    cursor = conexao.cursor()

    # A tabela de alunos precisa existir antes da tabela de notas.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            curso TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id_notas INTEGER PRIMARY KEY AUTOINCREMENT,
            id_aluno INTEGER NOT NULL,
            disciplina TEXT NOT NULL,
            sm1 REAL NOT NULL,
            sm2 REAL NOT NULL,
            av1 REAL NOT NULL,
            av2 REAL NOT NULL,
            FOREIGN KEY (id_aluno) REFERENCES alunos(id)
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

    cursor.execute("DELETE FROM notas WHERE id_aluno = ?", (id_aluno,))
    cursor.execute("DELETE FROM alunos WHERE id = ?", (id_aluno,))

    conexao.commit()
    conexao.close()

def inserir_notas(id_aluno, disciplina, sm1, sm2, av1, av2):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO notas (id_aluno, disciplina, sm1, sm2, av1, av2)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_aluno, disciplina, sm1, sm2, av1, av2))

    conexao.commit()
    conexao.close()

def listar_notas_por_aluno(id_aluno):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_notas, disciplina, sm1, sm2, av1, av2
        FROM notas
        WHERE id_aluno = ?
        ORDER BY id_notas
    """, (id_aluno,))
    notas = cursor.fetchall()

    conexao.close()
    return notas

def buscar_notas_por_id(id_notas):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM notas WHERE id_notas = ?", (id_notas,))
    notas = cursor.fetchone()

    conexao.close()
    return notas

def atualizar_notas(id_notas, disciplina, sm1, sm2, av1, av2):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE notas
        SET disciplina = ?, sm1 = ?, sm2 = ?, av1 = ?, av2 = ?
        WHERE id_notas = ?
    """, (disciplina, sm1, sm2, av1, av2, id_notas))

    conexao.commit()
    conexao.close()

def deletar_notas(id_notas):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM notas WHERE id_notas = ?", (id_notas,))

    conexao.commit()
    conexao.close()
