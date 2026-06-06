# Grupo de Desenvolvimento Rapido em Python

Projeto Extensionista da Faculdade Estacio de Sa - Niteroi (Unesa).

## Integrantes

- Jose Roberto Duarte Hegendorne - Matricula: 202502214154
- Rennan Ferreira de Almeida - Matricula: 202502211708
- Matheus Villela Duarte Ferreira - Matricula: 202503759537
- Pedro Vinicius Nogueira Sant'Anna - Matricula: 202503043681
- Igor Amaral dos Santos - Matricula: 202502260512

# Sistema de Cadastro de Alunos

## Descricao

Este projeto e um sistema CRUD desenvolvido em Python, utilizando SQLite como banco de dados e Tkinter para a interface grafica.

O sistema permite cadastrar alunos e registrar notas vinculadas ao aluno selecionado.

## Funcionalidades

- Cadastrar alunos
- Listar alunos
- Buscar alunos
- Atualizar alunos
- Excluir alunos
- Cadastrar notas por aluno
- Listar notas do aluno selecionado
- Atualizar notas
- Excluir notas

## Tecnologias utilizadas

- Python
- SQLite
- Tkinter

## Como executar o projeto

1. Abra o terminal na pasta do projeto.

2. Verifique se o Python esta instalado:

```bash
python --version
```

3. Execute o sistema pela interface grafica:

```bash
python interface.py
```

4. A janela do sistema sera aberta. Use a tabela de alunos para selecionar um aluno. Depois disso, a tabela de notas mostrara apenas as notas vinculadas a esse aluno.

## Observacao importante para abrir o sistema

O projeto deve ser aberto pelo arquivo `interface.py`.

Use:

```bash
python interface.py
```

## Banco de dados

O projeto usa o arquivo `sistema.db`, que fica na propria pasta do projeto.

Nao e necessario criar o banco manualmente. Quando o sistema inicia, a funcao `criar_tabela()` do arquivo `database.py` cria automaticamente as tabelas necessarias:

- `alunos`
- `notas`

As principais funcoes do banco estao no arquivo `database.py`, incluindo cadastro, listagem, atualizacao e exclusao de alunos e notas.

## Arquivos principais

- `interface.py`: arquivo usado para abrir a interface grafica do sistema.
- `database.py`: arquivo responsavel pela conexao com SQLite e pelas operacoes no banco.
- `sistema.db`: arquivo onde os dados ficam salvos.
- `integrantes.txt`: arquivo com os integrantes do grupo.
