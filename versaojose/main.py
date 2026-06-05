from database import (
    criando_sqlite,
    criando_postgree,
    inserir_aluno,
    listar_alunos,
    buscar_aluno_por_id,
    atualizar_aluno,
    deletar_aluno,
    config_db
)


def menu_db():
    print("\n===== Escolha seu banco de dados a ser usado =====")
    print("1 - Sqlite")
    print("2 - PostGree")
    print("0 - Sair")    

def menu():
    print("\n===== SISTEMA DE CADASTRO DE ALUNOS =====")
    print("1 - Cadastrar aluno")
    print("2 - Listar alunos")
    print("3 - Buscar aluno por ID")
    print("4 - Atualizar aluno")
    print("5 - Deletar aluno")
    print("0 - Sair")
2
def valida_id():
    while True:
        try:
            id_aluno = int(input("Digite o ID do aluno: "))
            return id_aluno
        except (ValueError, TypeError):
            print("============================================")
            print("=== Caracter inválido, digite novamente ===")
            print("============================================")

#Mensagem de não encontrado
# feito pelo josé
def mensagem_nao_encontrado():
        print("============================================")
        print("=== Aluno não encontrado, tente novamente ==")
        print("============================================")      
 
        
def cadastrar():
    nome = input("Nome do aluno: ")
    email = input("Email do aluno: ")
    curso = input("Curso do aluno: ")

    inserir_aluno(nome, email, curso)
    print("Aluno cadastrado com sucesso!")

def listar():
    alunos = listar_alunos()

    if not alunos:
        print("Nenhum aluno cadastrado.")
    else:
        print("\n--- Lista de alunos ---")
        for aluno in alunos:
            print(f"ID: {aluno[0]} | Nome: {aluno[1]} | Email: {aluno[2]} | Curso: {aluno[3]}")

def buscar():
    
    #feito pelo josé  função valida_id
    #id_aluno = int(input("Digite o ID do aluno: "))

    aluno = buscar_aluno_por_id(valida_id())

    if aluno:
        print(f"ID: {aluno[0]} | Nome: {aluno[1]} | Email: {aluno[2]} | Curso: {aluno[3]}")
    else:
        mensagem_nao_encontrado()


def atualizar():
    # atualização feita pelo josé
    #id_aluno = int(input("Digite o ID do aluno que deseja atualizar: "))
    aluno = buscar_aluno_por_id(valida_id())
  
    if aluno:
        
        nome = input("Novo nome: ")
        email = input("Novo email: ")
        curso = input("Novo curso: ")

        atualizar_aluno(aluno[0], nome, email, curso)
        print("Aluno atualizado com sucesso!")
    else:
       mensagem_nao_encontrado()

def deletar():
    #edição feita pelo josé
    #id_aluno = int(input("Digite o ID do aluno que deseja deletar: "))
    aluno = buscar_aluno_por_id(valida_id())

    if aluno:
        deletar_aluno(aluno[0])
        print("Aluno deletado com sucesso!")
    else:
        mensagem_nao_encontrado()

def main():
    config_db()

    if config_db():
        while True:
            menu()
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                cadastrar()
            elif opcao == "2":
                listar()
            elif opcao == "3":
                buscar()
            elif opcao == "4":
                atualizar()
            elif opcao == "5":
                deletar()
            elif opcao == "0":
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida. Tente novamente.")
    else:
         while True: 
            menu_db()   
            print("verificando base de dados")
            print("Database Inexistente!....")
            print("Dando inicio a instalacao do banco de dados")
            opcao = input("Escolha uma opcao: ")
            if opcao == "1":
                    criando_sqlite()
                    main()
                    return
            elif opcao == "2":
                    criando_postgree()
                    main()
                    return
            elif opcao == "0":
                    print("Saindo do sistema...")
                    break
            else:
                    print("Opcao invalida. Tente novamente.")


main()
