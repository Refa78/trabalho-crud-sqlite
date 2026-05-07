from database import (
    criar_tabela,
    inserir_aluno,
    listar_alunos,
    buscar_aluno_por_id,
    atualizar_aluno,
    deletar_aluno
)

def menu():
    print("\n===== SISTEMA DE CADASTRO DE ALUNOS =====")
    print("1 - Cadastrar aluno")
    print("2 - Listar alunos")
    print("3 - Buscar aluno por ID")
    print("4 - Atualizar aluno")
    print("5 - Deletar aluno")
    print("0 - Sair")

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
    id_aluno = int(input("Digite o ID do aluno: "))
    aluno = buscar_aluno_por_id(id_aluno)

    if aluno:
        print(f"ID: {aluno[0]} | Nome: {aluno[1]} | Email: {aluno[2]} | Curso: {aluno[3]}")
    else:
        print("Aluno não encontrado.")

def atualizar():
    id_aluno = int(input("Digite o ID do aluno que deseja atualizar: "))
    aluno = buscar_aluno_por_id(id_aluno)

    if aluno:
        nome = input("Novo nome: ")
        email = input("Novo email: ")
        curso = input("Novo curso: ")

        atualizar_aluno(id_aluno, nome, email, curso)
        print("Aluno atualizado com sucesso!")
    else:
        print("Aluno não encontrado.")

def deletar():
    id_aluno = int(input("Digite o ID do aluno que deseja deletar: "))
    aluno = buscar_aluno_por_id(id_aluno)

    if aluno:
        deletar_aluno(id_aluno)
        print("Aluno deletado com sucesso!")
    else:
        print("Aluno não encontrado.")

def main():
    criar_tabela()

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

main()