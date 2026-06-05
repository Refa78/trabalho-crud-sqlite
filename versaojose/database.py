import sqlite3
import os
import psycopg2
import configparser

#cria Banco de dados Postgree

def criando_postgree():
     while True:
            #criei um comando de repetição para caso erre as informações de cadastro ele volte a configurar

            #URL DO SERVIDOR
            print("=============================")
            host = input('Digite o endereço do banco: ')
            # NOME DO BANCO DE DADOS POSTGREE
            dataBase = input("Digite o nome da base de dados")
            # Login de acesso
            print("=============================")
            login = input("Digite o login: ")
            # senha do login
            print("=============================")
            Senha = input("Digite a senha: ")
            try:               
               #chama a conexão pelo psycopg2
               conexao = psycopg2.connect(host=host,database=dataBase,user=login,password=Senha, client_encoding='WIN1252')
               cursor = conexao.cursor()
               print("Funcionou a base", type(cursor))

               # Criando a tabela no banco de dados postgree
               
               cursor.execute("""
                                CREATE TABLE IF NOT EXISTS alunos (
                                    id SERIAL PRIMARY KEY,
                                    nome TEXT NOT NULL,
                                    email TEXT NOT NULL,
                                    curso TEXT NOT NULL
                                )
                            """)
               conexao.commit()
               conexao.close()   


               # Quando a conexão funcionar, salve os dados:
               config = configparser.ConfigParser()
               # Criando a seção dentro do arquivo
               config['POSTGRESQL'] = {
                  'host': host,
                  'database': dataBase,
                  'user': login,
                  'password': Senha
               }

               # Gravando efetivamente no arquivo conexao.ini
               with open('conexao.ini', 'w', encoding='utf-8') as arquivo_config:
                  config.write(arquivo_config)

               print("Configurações salvas com sucesso em conexao.ini!")

               break
            except psycopg2.OperationalError as e:
              print(f"Erro ao conectar: {e}")
              print("Digite 0 para Sair ou aperte enter para continuar")
              sair= input("Digite zero para sair do sistema ou enter para continuar")

              if sair == "0":
                    return
# Criando SQLite

def criando_sqlite():
    conexao = sqlite3.connect("sistema.db")
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


def conectar():
    if os.path.exists('conexao.ini'):
        # carrega o arquivo conexao.ini
        config = configparser.ConfigParser()
        # lendo o arquivo
        config.read('conexao.ini', encoding='utf-8')

        # Recuperando os valores salvos
        host = config['POSTGRESQL']['host']
        dataBase = config['POSTGRESQL']['database']
        login = config['POSTGRESQL']['user']
        Senha = config['POSTGRESQL']['password']
        return psycopg2.connect(host=host,database=dataBase,user=login,password=Senha, client_encoding='WIN1252')
    elif os.path.exists("sistema.db"):
         return sqlite3.connect("sistema.db")
    else:
          print("erro de conexao")
          
   
#  é chamado no inicio do man para saber o que tem para conectar    
def config_db():
    if os.path.exists('conexao.ini'):
        return True
    elif os.path.exists("sistema.db"):
        return True
    else: 
        return False 

           
# Insere Alunos
def inserir_aluno(nome, email, curso):
    conexao = conectar()
    cursor = conexao.cursor()
    if os.path.exists('conexao.ini'):
        cursor.execute("""
            INSERT INTO alunos (nome, email, curso)
            VALUES (%s, %s, %s)
          """, (nome, email, curso))
    else:
        cursor.execute("""
            INSERT INTO alunos (nome, email, curso)
            VALUES (?, ?, ?)
         """, (nome, email, curso))
        


    conexao.commit()
    conexao.close()
    
    
#lista alunos

def listar_alunos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM alunos")
    alunos = cursor.fetchall()

    conexao.close()
    return alunos

#busca alunos
def buscar_aluno_por_id(id_aluno):
    conexao = conectar()
    cursor = conexao.cursor()
    if os.path.exists('conexao.ini'):
        cursor.execute("SELECT * FROM alunos WHERE id = %s", (id_aluno,))
    else:
        cursor.execute("SELECT * FROM alunos WHERE id = ?", (id_aluno,))
    aluno = cursor.fetchone()

    conexao.close()
    return aluno

#Atualiza alunos
def atualizar_aluno(id_aluno,nome, email, curso):
    conexao = conectar()
    cursor = conexao.cursor()
    if os.path.exists('conexao.ini'):
        cursor.execute("""
                UPDATE alunos
                SET nome = %s, email = %s, curso = %s
                WHERE id = %s
            """, (nome, email, curso, id_aluno))
    else:    
        cursor.execute("""
            UPDATE alunos
            SET nome = ?, email = ?, curso = ?
            WHERE id = ?
        """, (nome, email, curso, id_aluno))

    conexao.commit()
    conexao.close()


#Deleta Alunos

def deletar_aluno(id_aluno):
    conexao = conectar()
    cursor = conexao.cursor()
    if os.path.exists('conexao.ini'):
         cursor.execute("DELETE FROM alunos WHERE id = %s", (id_aluno,))
    else:
        cursor.execute("DELETE FROM alunos WHERE id = ?",  (id_aluno,))
    conexao.commit()
    conexao.close()