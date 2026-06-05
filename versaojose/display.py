import tkinter as tk
from tkinter import ttk, messagebox

# Importa todas as funções do banco de dados criadas no database.py
from database import (
    criando_sqlite,       # Cria o banco SQLite local
    inserir_aluno,        # Insere um novo aluno no banco
    listar_alunos,        # Retorna todos os alunos cadastrados
    buscar_aluno_por_id,  # Busca um aluno específico pelo ID
    atualizar_aluno,      # Atualiza os dados de um aluno existente
    deletar_aluno,        # Remove um aluno do banco
    config_db,            # Verifica se já existe algum banco configurado
)

# ──────────────────────────────────────────────────────────────────
# PALETA DE CORES DA INTERFACE
# ──────────────────────────────────────────────────────────────────
BG       = "#1e1e2e"   # Fundo geral da janela
PANEL    = "#2a2a3d"   # Fundo dos painéis laterais
ACCENT   = "#7c6af7"   # Cor de destaque (botões principais, borda ativa)
ACCENT2  = "#5a4fcf"   # Cor de destaque ao passar o mouse
TEXT     = "#e8e6f0"   # Cor do texto principal
MUTED    = "#8885a0"   # Cor do texto secundário / labels
ENTRY_BG = "#13131f"   # Fundo dos campos de texto e da lista
SEL_BG   = "#3d3a5c"   # Fundo da linha selecionada na lista
DANGER   = "#e05c7a"   # Cor de alerta / botão excluir
SUCCESS  = "#4ecb8d"   # Cor de sucesso / botão cadastrar
BORDER   = "#3a3a55"   # Cor das bordas e separadores

# Fontes utilizadas na interface
FONT_HEAD  = ("Segoe UI", 13, "bold")  # Títulos de seção
FONT_BODY  = ("Segoe UI", 10)          # Texto geral e botões
FONT_SMALL = ("Segoe UI", 9)           # Labels secundários
FONT_MONO  = ("Consolas", 10)          # Exibição do ID selecionado


# ══════════════════════════════════════════════════════════════════
#  CLASSE: TelaEscolhaDB
#  Exibida na primeira execução, quando nenhum banco é encontrado.
#  Equivale ao menu_db() do main.py, mas em janela gráfica.
# ══════════════════════════════════════════════════════════════════
class TelaEscolhaDB(tk.Toplevel):

    def __init__(self, parent, callback):
        super().__init__(parent)
        # callback é a função que será chamada após o banco ser criado
        # para dar início à tela principal
        self.callback = callback

        self.title("Instalação do Banco de Dados")
        self.resizable(False, False)
        self.configure(bg=BG)

        self.construir_tela()
        self.centralizar_janela(420, 300)

        # Bloqueia interação com a janela pai enquanto esta estiver aberta
        self.grab_set()
        # Se o usuário fechar pelo X, encerra o programa
        self.protocol("WM_DELETE_WINDOW", self.sair)

    def centralizar_janela(self, largura, altura):
        """Posiciona a janela no centro da tela."""
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - largura)  // 2
        y = (self.winfo_screenheight() - altura) // 2
        self.geometry(f"{largura}x{altura}+{x}+{y}")

    def construir_tela(self):
        """Monta os widgets da tela de escolha do banco."""

        # Faixa colorida no topo
        tk.Frame(self, bg=ACCENT, height=6).pack(fill="x")

        # Título e instrução
        tk.Label(self, text="⚙  Instalação do Banco de Dados",
                 font=FONT_HEAD, bg=BG, fg=TEXT).pack(pady=(22, 6))
        tk.Label(self, text="Database Inexistente! Escolha o banco a configurar:",
                 font=FONT_SMALL, bg=BG, fg=MUTED).pack(pady=(0, 20))

        # Frame que agrupa os botões de escolha
        frame_botoes = tk.Frame(self, bg=BG)
        frame_botoes.pack(pady=6)

        # Botão 1 → chama criando_sqlite() do database.py
        self.criar_botao(frame_botoes,
                         "1 - SQLite  (local, sem servidor)",
                         self.escolher_sqlite).pack(fill="x", pady=6, ipady=10)

        # Botão 2 → chama criando_postgree() do database.py
        self.criar_botao(frame_botoes,
                         "2 - PostgreSQL  (servidor externo)",
                         self.escolher_postgree).pack(fill="x", pady=6, ipady=10)

        # Botão 0 → encerra o programa
        self.criar_botao(frame_botoes,
                         "0 - Sair",
                         self.sair, cor=DANGER).pack(fill="x", pady=6, ipady=6)

    def criar_botao(self, parent, texto, comando, cor=PANEL):
        """Cria e retorna um botão estilizado."""
        return tk.Button(
            parent, text=texto, command=comando,
            font=FONT_BODY, bg=cor, fg=TEXT,
            activebackground=ACCENT2, activeforeground="white",
            relief="flat", cursor="hand2", width=38,
            bd=0, highlightthickness=1, highlightbackground=BORDER
        )

    def escolher_sqlite(self):
        """
        Opção 1: banco local SQLite.
        Chama criando_sqlite() do database.py, que cria o arquivo sistema.db
        e a tabela 'alunos' se ainda não existirem.
        """
        criando_sqlite()
        self.destroy()
        self.callback()  # Abre a tela principal

    def escolher_postgree(self):
        """
        Opção 2: banco PostgreSQL.
        Em vez de chamar criando_postgree() (que usa input() no terminal),
        abre a janela gráfica TelaConfigPostgree para coletar os dados
        de conexão em campos de texto visuais.
        """
        # Passa o master (App) e o callback para a nova janela poder
        # abrir a tela principal após a configuração ser concluída
        TelaConfigPostgree(self.master, self.callback)
        self.destroy()

    def sair(self):
        """Encerra o programa inteiro ao fechar esta janela."""
        self.master.destroy()


# ══════════════════════════════════════════════════════════════════
#  CLASSE: TelaConfigPostgree
#  Formulário gráfico para configurar a conexão PostgreSQL.
#  Substitui o loop de input() que existe em criando_postgree()
#  do database.py, mantendo exatamente a mesma lógica de conexão
#  e gravação do arquivo conexao.ini.
# ══════════════════════════════════════════════════════════════════
class TelaConfigPostgree(tk.Toplevel):

    def __init__(self, parent, callback):
        super().__init__(parent)
        # callback é chamado após conexão bem-sucedida para abrir o app
        self.callback = callback

        self.title("Configurar PostgreSQL")
        self.resizable(False, False)
        self.configure(bg=BG)

        self.construir_tela()
        self.centralizar_janela(420, 400)

        # Bloqueia a janela pai enquanto esta estiver aberta
        self.grab_set()
        # Fechar pelo X volta para a tela de escolha do banco
        self.protocol("WM_DELETE_WINDOW", self.voltar)

    def centralizar_janela(self, largura, altura):
        """Posiciona a janela no centro da tela."""
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - largura)  // 2
        y = (self.winfo_screenheight() - altura) // 2
        self.geometry(f"{largura}x{altura}+{x}+{y}")

    def construir_tela(self):
        """Monta o formulário com os campos de conexão PostgreSQL."""

        # Faixa colorida no topo
        tk.Frame(self, bg=ACCENT, height=6).pack(fill="x")

        # Título
        tk.Label(self, text="🐘  Configurar PostgreSQL",
                 font=FONT_HEAD, bg=BG, fg=TEXT).pack(pady=(20, 4))
        tk.Label(self, text="Preencha os dados de conexão com o servidor:",
                 font=FONT_SMALL, bg=BG, fg=MUTED).pack(pady=(0, 16))

        # Frame do formulário com padding lateral
        form = tk.Frame(self, bg=BG)
        form.pack(fill="x", padx=30)

        # Campos de entrada — cada um retorna uma StringVar
        self.campo_host  = self.criar_campo(form, "🌐  Host / Endereço do servidor")
        self.campo_banco = self.criar_campo(form, "🗄  Nome do banco de dados")
        self.campo_login = self.criar_campo(form, "👤  Usuário / Login")
        self.campo_senha = self.criar_campo(form, "🔒  Senha", ocultar=True)

        # Botão de conectar
        tk.Button(
            self, text="Conectar e Salvar",
            command=self.conectar,
            font=FONT_BODY, bg=ACCENT, fg="white",
            activebackground=ACCENT2, activeforeground="white",
            relief="flat", cursor="hand2", bd=0, pady=10
        ).pack(fill="x", padx=30, pady=(16, 6))

        # Botão de voltar
        tk.Button(
            self, text="← Voltar",
            command=self.voltar,
            font=FONT_SMALL, bg=PANEL, fg=MUTED,
            activebackground=BORDER, activeforeground=TEXT,
            relief="flat", cursor="hand2", bd=0, pady=6,
            highlightthickness=1, highlightbackground=BORDER
        ).pack(fill="x", padx=30, pady=(0, 16))

    def criar_campo(self, parent, label, ocultar=False):
        """
        Cria um label + Entry dentro do frame do formulário.
        ocultar=True exibe '●' no lugar dos caracteres (para senha).
        Retorna a StringVar vinculada ao campo.
        """
        tk.Label(parent, text=label, font=FONT_SMALL,
                 bg=BG, fg=MUTED, anchor="w").pack(fill="x", pady=(6, 1))
        variavel = tk.StringVar()
        tk.Entry(
            parent, textvariable=variavel, font=FONT_BODY,
            bg=ENTRY_BG, fg=TEXT, insertbackground=ACCENT,
            relief="flat", bd=8,
            show="●" if ocultar else "",
            highlightthickness=1, highlightbackground=BORDER,
            highlightcolor=ACCENT
        ).pack(fill="x", pady=(0, 4))
        return variavel

    def conectar(self):
        """
        Lê os campos, testa a conexão com psycopg2 e, se bem-sucedida:
          1. Cria a tabela 'alunos' se não existir (igual a criando_postgree())
          2. Salva as credenciais no arquivo conexao.ini
          3. Fecha esta janela e abre a tela principal via callback
        Em caso de erro, exibe a mensagem e permite corrigir os dados.
        """
        import configparser
        import psycopg2

        # Lê e valida os campos
        host  = self.campo_host.get().strip()
        banco = self.campo_banco.get().strip()
        login = self.campo_login.get().strip()
        senha = self.campo_senha.get()

        if not all([host, banco, login, senha]):
            messagebox.showwarning("Campos obrigatórios",
                                    "Preencha todos os campos antes de conectar.",
                                    parent=self)
            return

        try:
            # Testa a conexão com os dados informados
            conexao = psycopg2.connect(
                host=host, database=banco,
                user=login, password=senha,
                client_encoding="WIN1252"
            )
            cursor = conexao.cursor()

            # Cria a tabela alunos se ainda não existir
            # (mesma estrutura usada em criando_postgree() do database.py)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alunos (
                    id    SERIAL PRIMARY KEY,
                    nome  TEXT NOT NULL,
                    email TEXT NOT NULL,
                    curso TEXT NOT NULL
                )
            """)
            conexao.commit()
            conexao.close()

            # Salva as credenciais no arquivo conexao.ini
            # (mesmo formato lido por conectar() no database.py)
            config = configparser.ConfigParser()
            config["POSTGRESQL"] = {
                "host":     host,
                "database": banco,
                "user":     login,
                "password": senha,
            }
            with open("conexao.ini", "w", encoding="utf-8") as arquivo:
                config.write(arquivo)

            messagebox.showinfo("Conexão estabelecida",
                                 "PostgreSQL configurado com sucesso!",
                                 parent=self)
            self.destroy()
            self.callback()  # Abre a tela principal

        except psycopg2.OperationalError as erro:
            # Exibe o erro e mantém a janela aberta para correção
            messagebox.showerror("Erro de conexão",
                                  f"Não foi possível conectar:\n\n{erro}",
                                  parent=self)

    def voltar(self):
        """Fecha esta janela e reabre a tela de escolha do banco."""
        self.destroy()
        TelaEscolhaDB(self.master, self.callback)


# ══════════════════════════════════════════════════════════════════
#  CLASSE: App  (janela principal)
#  Contém o formulário de cadastro e a lista de alunos.
#  Todas as operações de banco chamam as funções do database.py.
# ══════════════════════════════════════════════════════════════════
class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Sistema de Cadastro de Alunos")
        self.configure(bg=BG)
        self.minsize(860, 560)
        self.centralizar_janela(920, 630)

        # Guarda o ID do aluno selecionado na lista (None = nenhum)
        self.id_selecionado = None

        # Verifica se já existe banco configurado (SQLite ou PostgreSQL)
        if not config_db():
            # Primeira execução: esconde a janela principal e abre
            # o menu de escolha do banco
            self.withdraw()
            TelaEscolhaDB(self, self.iniciar_aplicacao)
        else:
            # Banco já existe: inicia direto
            self.iniciar_aplicacao()

    def centralizar_janela(self, largura, altura):
        """Posiciona a janela principal no centro da tela."""
        x = (self.winfo_screenwidth()  - largura)  // 2
        y = (self.winfo_screenheight() - altura) // 2
        self.geometry(f"{largura}x{altura}+{x}+{y}")

    def iniciar_aplicacao(self):
        """
        Ponto de entrada após o banco estar pronto.
        Constrói a interface e carrega os alunos na lista.
        """
        self.deiconify()           # Exibe a janela principal
        self.construir_interface() # Monta todos os widgets
        self.recarregar_lista()    # Carrega registros do banco na Treeview

    # ──────────────────────────────────────────────────────────────
    # CONSTRUÇÃO DA INTERFACE
    # ──────────────────────────────────────────────────────────────

    def construir_interface(self):
        """Monta a barra superior e os dois painéis (formulário + lista)."""
        import os

        # Remove widgets anteriores (caso a janela seja reiniciada)
        for widget in self.winfo_children():
            widget.destroy()

        # ── Barra superior ──────────────────────────────────────
        barra_topo = tk.Frame(self, bg=ACCENT, height=50)
        barra_topo.pack(fill="x")
        barra_topo.pack_propagate(False)

        tk.Label(barra_topo, text="  🎓  Sistema de Cadastro de Alunos",
                 font=FONT_HEAD, bg=ACCENT, fg="white").pack(side="left", padx=10)

        # Indica qual banco está em uso no canto superior direito
        tipo_banco = "PostgreSQL" if os.path.exists("conexao.ini") else "SQLite"
        tk.Label(barra_topo, text=f"● {tipo_banco}", font=FONT_SMALL,
                 bg=ACCENT, fg="#d4d0ff").pack(side="right", padx=16)

        # ── Corpo principal (dois painéis lado a lado) ───────────
        corpo = tk.Frame(self, bg=BG)
        corpo.pack(fill="both", expand=True, padx=16, pady=12)

        self.construir_formulario(corpo)  # Painel esquerdo
        self.construir_lista(corpo)       # Painel direito

    def construir_formulario(self, parent):
        """
        Painel esquerdo: campos de texto e botões de ação.
        Cada botão chama um método que, por sua vez, chama
        a função correspondente no database.py.
        """
        painel = tk.Frame(parent, bg=PANEL,
                          highlightthickness=1, highlightbackground=BORDER)
        painel.pack(side="left", fill="y", padx=(0, 10), ipadx=14, ipady=14)

        # Título do painel
        tk.Label(painel, text="Dados do Aluno", font=FONT_HEAD,
                 bg=PANEL, fg=TEXT).pack(pady=(16, 14), padx=20, anchor="w")

        # Campos de entrada — cada um retorna uma StringVar vinculada ao Entry
        self.campo_nome  = self.criar_campo(painel, "👤  Nome")
        self.campo_email = self.criar_campo(painel, "✉  Email")
        self.campo_curso = self.criar_campo(painel, "📚  Curso")

        # Linha que exibe o ID do registro atualmente selecionado
        linha_id = tk.Frame(painel, bg=PANEL)
        linha_id.pack(fill="x", padx=20, pady=(6, 14))
        tk.Label(linha_id, text="ID selecionado:", font=FONT_SMALL,
                 bg=PANEL, fg=MUTED).pack(side="left")
        self.label_id = tk.Label(linha_id, text="—", font=FONT_MONO,
                                  bg=PANEL, fg=ACCENT)
        self.label_id.pack(side="left", padx=8)

        # Separador visual
        tk.Frame(painel, bg=BORDER, height=1).pack(fill="x", padx=20, pady=(0, 12))

        # ── Botões de ação ──────────────────────────────────────
        # Cadastrar → inserir_aluno()
        self.criar_botao(painel, "➕  Cadastrar",    SUCCESS, self.acao_cadastrar)
        # Atualizar → atualizar_aluno()
        self.criar_botao(painel, "✏  Atualizar",     ACCENT,  self.acao_atualizar)
        # Excluir   → deletar_aluno()
        self.criar_botao(painel, "🗑  Excluir",       DANGER,  self.acao_excluir)
        # Buscar    → buscar_aluno_por_id()
        self.criar_botao(painel, "🔍  Buscar por ID", PANEL,   self.acao_buscar, borda=ACCENT)

        # Separador
        tk.Frame(painel, bg=BORDER, height=1).pack(fill="x", padx=20, pady=10)

        # Limpar campos (não acessa o banco, apenas reseta a tela)
        self.criar_botao(painel, "✖  Limpar campos", PANEL, self.limpar_campos, borda=BORDER)

    def criar_campo(self, parent, label):
        """
        Cria um label + Entry e retorna a StringVar vinculada ao campo.
        Usado para Nome, Email e Curso.
        """
        tk.Label(parent, text=label, font=FONT_SMALL,
                 bg=PANEL, fg=MUTED, anchor="w").pack(fill="x", padx=20, pady=(6, 1))
        variavel = tk.StringVar()
        tk.Entry(parent, textvariable=variavel, font=FONT_BODY,
                 bg=ENTRY_BG, fg=TEXT, insertbackground=ACCENT,
                 relief="flat", bd=8,
                 highlightthickness=1, highlightbackground=BORDER,
                 highlightcolor=ACCENT).pack(fill="x", padx=20)
        return variavel

    def criar_botao(self, parent, texto, cor_fundo, comando, borda=None):
        """Cria e empacota um botão estilizado no painel do formulário."""
        extras = {"highlightthickness": 1, "highlightbackground": borda} if borda else {}
        tk.Button(
            parent, text=texto, command=comando,
            font=FONT_BODY, bg=cor_fundo, fg=TEXT,
            activebackground=ACCENT2, activeforeground="white",
            relief="flat", cursor="hand2", bd=0, pady=8,
            **extras
        ).pack(fill="x", padx=20, pady=3)

    def construir_lista(self, parent):
        """
        Painel direito: campo de busca rápida e Treeview com todos os alunos.
        Ao clicar em uma linha, os dados são carregados no formulário.
        """
        painel = tk.Frame(parent, bg=PANEL,
                          highlightthickness=1, highlightbackground=BORDER)
        painel.pack(side="left", fill="both", expand=True, ipadx=6, ipady=6)

        # Cabeçalho do painel com contador de registros
        cabecalho = tk.Frame(painel, bg=PANEL)
        cabecalho.pack(fill="x", padx=12, pady=(14, 6))
        tk.Label(cabecalho, text="Lista de Alunos", font=FONT_HEAD,
                 bg=PANEL, fg=TEXT).pack(side="left")
        self.label_total = tk.Label(cabecalho, text="0 registros",
                                     font=FONT_SMALL, bg=PANEL, fg=MUTED)
        self.label_total.pack(side="right")

        # ── Campo de busca rápida ───────────────────────────────
        # Filtra a lista exibida sem fazer nova consulta ao banco
        linha_busca = tk.Frame(painel, bg=PANEL)
        linha_busca.pack(fill="x", padx=12, pady=(0, 8))
        tk.Label(linha_busca, text="🔎", bg=PANEL, fg=MUTED,
                 font=FONT_BODY).pack(side="left")
        self.campo_busca = tk.StringVar()
        # trace_add dispara filtrar_lista() a cada caractere digitado
        self.campo_busca.trace_add("write", lambda *_: self.filtrar_lista())
        tk.Entry(linha_busca, textvariable=self.campo_busca, font=FONT_BODY,
                 bg=ENTRY_BG, fg=TEXT, insertbackground=ACCENT,
                 relief="flat", bd=6,
                 highlightthickness=1, highlightbackground=BORDER,
                 highlightcolor=ACCENT).pack(side="left", fill="x",
                                              expand=True, padx=(6, 0))

        # ── Treeview (tabela de registros) ──────────────────────
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Alunos.Treeview",
                          background=ENTRY_BG, fieldbackground=ENTRY_BG,
                          foreground=TEXT, rowheight=30,
                          font=FONT_BODY, borderwidth=0)
        estilo.configure("Alunos.Treeview.Heading",
                          background=PANEL, foreground=MUTED,
                          font=FONT_SMALL, relief="flat")
        estilo.map("Alunos.Treeview",
                   background=[("selected", SEL_BG)],
                   foreground=[("selected", TEXT)])

        colunas = ("id", "nome", "email", "curso")
        self.tabela = ttk.Treeview(painel, columns=colunas, show="headings",
                                    style="Alunos.Treeview", selectmode="browse")

        # Define cabeçalho e largura de cada coluna
        for coluna, largura, alinhamento in [
            ("id",    50,  "center"),
            ("nome",  180, "w"),
            ("email", 210, "w"),
            ("curso", 150, "w"),
        ]:
            self.tabela.heading(coluna, text=coluna.upper())
            self.tabela.column(coluna, width=largura, anchor=alinhamento, minwidth=40)

        # Scrollbar vertical vinculada à Treeview
        barra_rolagem = ttk.Scrollbar(painel, orient="vertical",
                                       command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=barra_rolagem.set)

        self.tabela.pack(side="left", fill="both", expand=True,
                          padx=(12, 0), pady=(0, 12))
        barra_rolagem.pack(side="left", fill="y", pady=(0, 12), padx=(0, 6))

        # Ao selecionar uma linha, preenche o formulário com os dados dela
        self.tabela.bind("<<TreeviewSelect>>", self.ao_selecionar_linha)

    # ──────────────────────────────────────────────────────────────
    # GERENCIAMENTO DA LISTA
    # ──────────────────────────────────────────────────────────────

    def recarregar_lista(self):
        """
        Consulta todos os alunos via listar_alunos() do database.py
        e atualiza a Treeview com os dados mais recentes.
        """
        self.todos_alunos = listar_alunos()  # Busca no banco
        self.preencher_tabela(self.todos_alunos)

    def preencher_tabela(self, alunos):
        """
        Limpa a Treeview e insere a lista de alunos recebida.
        Também atualiza o contador de registros exibido no cabeçalho.
        """
        # Remove todas as linhas existentes
        for linha in self.tabela.get_children():
            self.tabela.delete(linha)

        # Insere cada aluno como uma nova linha
        # iid=str(aluno[0]) permite localizar a linha pelo ID
        for aluno in alunos:
            self.tabela.insert("", "end", iid=str(aluno[0]), values=aluno)

        # Atualiza contador
        total = len(alunos)
        self.label_total.config(text=f"{total} registro{'s' if total != 1 else ''}")

    def filtrar_lista(self):
        """
        Filtra a Treeview localmente (sem consultar o banco novamente)
        com base no texto digitado no campo de busca rápida.
        Busca em todas as colunas: ID, nome, email e curso.
        """
        termo = self.campo_busca.get().lower()
        if not termo:
            # Sem filtro: exibe todos os alunos
            self.preencher_tabela(self.todos_alunos)
            return
        # Mantém apenas os alunos que contêm o termo em qualquer coluna
        filtrados = [
            aluno for aluno in self.todos_alunos
            if any(termo in str(valor).lower() for valor in aluno)
        ]
        self.preencher_tabela(filtrados)

    def ao_selecionar_linha(self, event):
        """
        Disparado ao clicar em uma linha da Treeview.
        Lê os valores da linha selecionada e preenche
        os campos do formulário para facilitar edição.
        """
        selecao = self.tabela.selection()
        if not selecao:
            return

        valores = self.tabela.item(selecao[0], "values")
        if not valores:
            return

        # Armazena o ID e preenche cada campo do formulário
        self.id_selecionado = int(valores[0])
        self.label_id.config(text=str(valores[0]))
        self.campo_nome.set(valores[1])
        self.campo_email.set(valores[2])
        self.campo_curso.set(valores[3])

    # ──────────────────────────────────────────────────────────────
    # AÇÕES DO FORMULÁRIO  (cada uma chama uma função do database.py)
    # ──────────────────────────────────────────────────────────────

    def campos_preenchidos(self):
        """
        Valida se Nome, Email e Curso foram preenchidos.
        Retorna True se tudo OK, False e exibe aviso caso contrário.
        """
        if not self.campo_nome.get().strip():
            messagebox.showwarning("Campo obrigatório", "Informe o nome do aluno.")
            return False
        if not self.campo_email.get().strip():
            messagebox.showwarning("Campo obrigatório", "Informe o e-mail do aluno.")
            return False
        if not self.campo_curso.get().strip():
            messagebox.showwarning("Campo obrigatório", "Informe o curso do aluno.")
            return False
        return True

    def acao_cadastrar(self):
        """
        Botão CADASTRAR.
        Valida os campos e chama inserir_aluno() do database.py.
        Após inserir, limpa o formulário e recarrega a lista.
        """
        if not self.campos_preenchidos():
            return

        inserir_aluno(
            self.campo_nome.get().strip(),
            self.campo_email.get().strip(),
            self.campo_curso.get().strip()
        )

        self.limpar_campos()
        self.recarregar_lista()
        messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")

    def acao_atualizar(self):
        """
        Botão ATUALIZAR.
        Exige que um aluno esteja selecionado na lista.
        Chama atualizar_aluno() do database.py com o ID selecionado
        e os novos valores dos campos.
        """
        if self.id_selecionado is None:
            messagebox.showwarning("Nenhum aluno selecionado",
                                    "Clique em um aluno na lista antes de atualizar.")
            return
        if not self.campos_preenchidos():
            return

        atualizar_aluno(
            self.id_selecionado,
            self.campo_nome.get().strip(),
            self.campo_email.get().strip(),
            self.campo_curso.get().strip()
        )

        self.recarregar_lista()
        messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")

    def acao_excluir(self):
        """
        Botão EXCLUIR.
        Exige que um aluno esteja selecionado na lista.
        Pede confirmação antes de chamar deletar_aluno() do database.py.
        Após excluir, limpa o formulário e recarrega a lista.
        """
        if self.id_selecionado is None:
            messagebox.showwarning("Nenhum aluno selecionado",
                                    "Clique em um aluno na lista antes de excluir.")
            return

        nome = self.campo_nome.get() or f"ID {self.id_selecionado}"
        confirmado = messagebox.askyesno(
            "Confirmar exclusão",
            f'Deseja realmente excluir o aluno "{nome}"?'
        )
        if not confirmado:
            return

        deletar_aluno(self.id_selecionado)

        self.limpar_campos()
        self.recarregar_lista()
        messagebox.showinfo("Sucesso", "Aluno excluído com sucesso!")

    def acao_buscar(self):
        """
        Botão BUSCAR POR ID.
        Usa o ID do aluno atualmente selecionado na lista e chama
        buscar_aluno_por_id() do database.py para confirmar/recarregar
        os dados nos campos do formulário.
        """
        if self.id_selecionado is None:
            messagebox.showwarning("Nenhum ID selecionado",
                                    "Selecione um aluno na lista primeiro.")
            return

        aluno = buscar_aluno_por_id(self.id_selecionado)

        if aluno:
            # Preenche o formulário com os dados retornados do banco
            self.label_id.config(text=str(aluno[0]))
            self.campo_nome.set(aluno[1])
            self.campo_email.set(aluno[2])
            self.campo_curso.set(aluno[3])
            # Destaca a linha correspondente na Treeview
            try:
                self.tabela.selection_set(str(aluno[0]))
                self.tabela.see(str(aluno[0]))
            except Exception:
                pass
        else:
            messagebox.showwarning("Não encontrado",
                                    f"Nenhum aluno com ID {self.id_selecionado}.")

    def limpar_campos(self):
        """
        Reseta o formulário: apaga os campos de texto,
        limpa o ID selecionado e remove o destaque da lista.
        Não acessa o banco de dados.
        """
        self.id_selecionado = None
        self.label_id.config(text="—")
        self.campo_nome.set("")
        self.campo_email.set("")
        self.campo_curso.set("")
        self.tabela.selection_remove(self.tabela.selection())


# ══════════════════════════════════════════════════════════════════
#  PONTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()