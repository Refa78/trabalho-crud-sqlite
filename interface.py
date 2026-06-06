import tkinter as tk
from tkinter import ttk, messagebox

from database import (
    atualizar_aluno,
    atualizar_notas,
    buscar_aluno_por_id,
    criar_tabela,
    deletar_aluno,
    deletar_notas,
    inserir_aluno,
    inserir_notas,
    listar_alunos,
    listar_notas_por_aluno,
)

# Paleta da interface antiga.
BG = "#1e1e2e"
PANEL = "#2a2a3d"
ACCENT = "#7c6af7"
ACCENT2 = "#5a4fcf"
TEXT = "#e8e6f0"
MUTED = "#8885a0"
ENTRY_BG = "#13131f"
SEL_BG = "#3d3a5c"
DANGER = "#e05c7a"
SUCCESS = "#4ecb8d"
BORDER = "#3a3a55"

FONT_HEAD = ("Segoe UI", 13, "bold")
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
FONT_MONO = ("Consolas", 10)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        criar_tabela()

        self.title("Sistema de Cadastro de Alunos - SQLite")
        self.configure(bg=BG)
        self.minsize(980, 650)
        self.centralizar_janela(1120, 720)

        self.alunos = []
        self.notas = []
        self.id_aluno_selecionado = None
        self.id_nota_selecionada = None

        self.configurar_estilos()
        self.montar_interface()
        self.recarregar_alunos()

    def centralizar_janela(self, largura, altura):
        x = (self.winfo_screenwidth() - largura) // 2
        y = (self.winfo_screenheight() - altura) // 2
        self.geometry(f"{largura}x{altura}+{x}+{y}")

    def configurar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "Dark.Treeview",
            background=ENTRY_BG,
            fieldbackground=ENTRY_BG,
            foreground=TEXT,
            rowheight=30,
            font=FONT_BODY,
            borderwidth=0,
        )
        estilo.configure(
            "Dark.Treeview.Heading",
            background=PANEL,
            foreground=MUTED,
            font=FONT_SMALL,
            relief="flat",
        )
        estilo.map(
            "Dark.Treeview",
            background=[("selected", SEL_BG)],
            foreground=[("selected", TEXT)],
        )
        estilo.configure(
            "Vertical.TScrollbar",
            background=PANEL,
            troughcolor=ENTRY_BG,
            bordercolor=BORDER,
            arrowcolor=TEXT,
        )

    def montar_interface(self):
        barra_topo = tk.Frame(self, bg=ACCENT, height=56)
        barra_topo.pack(fill="x")
        barra_topo.pack_propagate(False)

        tk.Label(
            barra_topo,
            text="Sistema de Cadastro de Alunos",
            font=FONT_TITLE,
            bg=ACCENT,
            fg="white",
        ).pack(side="left", padx=18)

        tk.Label(
            barra_topo,
            text="SQLite",
            font=FONT_SMALL,
            bg=ACCENT,
            fg="#d4d0ff",
        ).pack(side="right", padx=18)

        corpo = tk.Frame(self, bg=BG)
        corpo.pack(fill="both", expand=True, padx=16, pady=14)

        self.montar_painel_resumo(corpo)
        self.montar_area_principal(corpo)

    def montar_painel_resumo(self, parent):
        painel = tk.Frame(
            parent,
            bg=PANEL,
            width=250,
            highlightthickness=1,
            highlightbackground=BORDER,
        )
        painel.pack(side="left", fill="y", padx=(0, 12))
        painel.pack_propagate(False)

        tk.Label(
            painel,
            text="Aluno selecionado",
            font=FONT_HEAD,
            bg=PANEL,
            fg=TEXT,
        ).pack(anchor="w", padx=18, pady=(18, 10))

        self.label_id_aluno = self.criar_linha_resumo(painel, "ID", "-")
        self.label_nome_aluno = self.criar_linha_resumo(painel, "Nome", "-")
        self.label_email_aluno = self.criar_linha_resumo(painel, "Email", "-")
        self.label_curso_aluno = self.criar_linha_resumo(painel, "Curso", "-")

        tk.Frame(painel, bg=BORDER, height=1).pack(fill="x", padx=18, pady=14)

        self.criar_botao(painel, "Novo aluno", SUCCESS, self.abrir_janela_novo_aluno)
        self.criar_botao(painel, "Editar aluno", ACCENT, self.abrir_janela_editar_aluno)
        self.criar_botao(painel, "Excluir aluno", DANGER, self.excluir_aluno)

        tk.Frame(painel, bg=BORDER, height=1).pack(fill="x", padx=18, pady=14)

        self.criar_botao(painel, "Cadastrar notas", SUCCESS, self.abrir_janela_nova_nota)
        self.criar_botao(painel, "Editar notas", ACCENT, self.abrir_janela_editar_nota)
        self.criar_botao(painel, "Excluir notas", DANGER, self.excluir_nota)

        tk.Frame(painel, bg=BORDER, height=1).pack(fill="x", padx=18, pady=14)
        self.criar_botao(painel, "Atualizar listas", PANEL, self.atualizar_tudo, borda=BORDER)

    def criar_linha_resumo(self, parent, titulo, valor):
        tk.Label(
            parent,
            text=titulo,
            font=FONT_SMALL,
            bg=PANEL,
            fg=MUTED,
        ).pack(anchor="w", padx=18, pady=(8, 0))

        label = tk.Label(
            parent,
            text=valor,
            font=FONT_MONO,
            bg=PANEL,
            fg=TEXT,
            wraplength=210,
            justify="left",
        )
        label.pack(anchor="w", padx=18)
        return label

    def montar_area_principal(self, parent):
        area = tk.Frame(parent, bg=BG)
        area.pack(side="left", fill="both", expand=True)

        self.montar_tabela_alunos(area)
        self.montar_tabela_notas(area)

    def montar_tabela_alunos(self, parent):
        painel = self.criar_painel(parent)
        painel.pack(fill="both", expand=True, pady=(0, 12))

        cabecalho = tk.Frame(painel, bg=PANEL)
        cabecalho.pack(fill="x", padx=14, pady=(12, 8))

        tk.Label(
            cabecalho,
            text="Alunos cadastrados",
            font=FONT_HEAD,
            bg=PANEL,
            fg=TEXT,
        ).pack(side="left")

        self.label_total_alunos = tk.Label(
            cabecalho,
            text="0 registros",
            font=FONT_SMALL,
            bg=PANEL,
            fg=MUTED,
        )
        self.label_total_alunos.pack(side="right")

        linha_busca = tk.Frame(painel, bg=PANEL)
        linha_busca.pack(fill="x", padx=14, pady=(0, 10))

        tk.Label(linha_busca, text="Buscar:", font=FONT_SMALL, bg=PANEL, fg=MUTED).pack(side="left")
        self.busca_aluno = tk.StringVar()
        self.busca_aluno.trace_add("write", lambda *_: self.filtrar_alunos())
        self.criar_entry(linha_busca, self.busca_aluno).pack(side="left", fill="x", expand=True, padx=(8, 0))

        frame_tabela = tk.Frame(painel, bg=PANEL)
        frame_tabela.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        colunas = ("id", "nome", "email", "curso")
        self.tabela_alunos = ttk.Treeview(
            frame_tabela,
            columns=colunas,
            show="headings",
            style="Dark.Treeview",
            selectmode="browse",
        )
        self.tabela_alunos.heading("id", text="ID")
        self.tabela_alunos.heading("nome", text="NOME")
        self.tabela_alunos.heading("email", text="EMAIL")
        self.tabela_alunos.heading("curso", text="CURSO")
        self.tabela_alunos.column("id", width=60, anchor="center")
        self.tabela_alunos.column("nome", width=220, anchor="w")
        self.tabela_alunos.column("email", width=260, anchor="w")
        self.tabela_alunos.column("curso", width=180, anchor="w")

        barra = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tabela_alunos.yview)
        self.tabela_alunos.configure(yscrollcommand=barra.set)
        self.tabela_alunos.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        self.tabela_alunos.bind("<<TreeviewSelect>>", self.selecionar_aluno)
        self.tabela_alunos.bind("<Double-1>", lambda event: self.abrir_janela_editar_aluno())

    def montar_tabela_notas(self, parent):
        painel = self.criar_painel(parent)
        painel.pack(fill="both", expand=True)

        cabecalho = tk.Frame(painel, bg=PANEL)
        cabecalho.pack(fill="x", padx=14, pady=(12, 8))

        self.label_titulo_notas = tk.Label(
            cabecalho,
            text="Notas do aluno selecionado",
            font=FONT_HEAD,
            bg=PANEL,
            fg=TEXT,
        )
        self.label_titulo_notas.pack(side="left")

        self.label_total_notas = tk.Label(
            cabecalho,
            text="0 notas",
            font=FONT_SMALL,
            bg=PANEL,
            fg=MUTED,
        )
        self.label_total_notas.pack(side="right")

        frame_tabela = tk.Frame(painel, bg=PANEL)
        frame_tabela.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        colunas = ("id", "disciplina", "sm1", "sm2", "av1", "av2")
        self.tabela_notas = ttk.Treeview(
            frame_tabela,
            columns=colunas,
            show="headings",
            style="Dark.Treeview",
            selectmode="browse",
        )
        for coluna, texto, largura in [
            ("id", "ID", 60),
            ("disciplina", "DISCIPLINA", 220),
            ("sm1", "SIMULADO 1", 120),
            ("sm2", "SIMULADO 2", 120),
            ("av1", "AVALIACAO 1", 120),
            ("av2", "AVALIACAO 2", 120),
        ]:
            self.tabela_notas.heading(coluna, text=texto)
            self.tabela_notas.column(coluna, width=largura, anchor="center")
        self.tabela_notas.column("disciplina", anchor="w")

        barra = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tabela_notas.yview)
        self.tabela_notas.configure(yscrollcommand=barra.set)
        self.tabela_notas.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        self.tabela_notas.bind("<<TreeviewSelect>>", self.selecionar_nota)
        self.tabela_notas.bind("<Double-1>", lambda event: self.abrir_janela_editar_nota())

    def criar_painel(self, parent):
        return tk.Frame(
            parent,
            bg=PANEL,
            highlightthickness=1,
            highlightbackground=BORDER,
        )

    def criar_entry(self, parent, variavel=None):
        return tk.Entry(
            parent,
            textvariable=variavel,
            font=FONT_BODY,
            bg=ENTRY_BG,
            fg=TEXT,
            insertbackground=ACCENT,
            relief="flat",
            bd=7,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
        )

    def criar_botao(self, parent, texto, cor, comando, borda=None):
        extras = {"highlightthickness": 1, "highlightbackground": borda} if borda else {}
        botao = tk.Button(
            parent,
            text=texto,
            command=comando,
            font=FONT_BODY,
            bg=cor,
            fg=TEXT,
            activebackground=ACCENT2,
            activeforeground="white",
            relief="flat",
            bd=0,
            pady=9,
            cursor="hand2",
            **extras,
        )
        botao.pack(fill="x", padx=18, pady=4)
        return botao

    def recarregar_alunos(self):
        self.alunos = listar_alunos()
        self.preencher_alunos(self.alunos)

    def preencher_alunos(self, alunos):
        self.tabela_alunos.delete(*self.tabela_alunos.get_children())
        for aluno in alunos:
            self.tabela_alunos.insert("", "end", iid=str(aluno[0]), values=aluno)
        total = len(alunos)
        self.label_total_alunos.config(text=f"{total} registro{'s' if total != 1 else ''}")

    def filtrar_alunos(self):
        termo = self.busca_aluno.get().strip().lower()
        if not termo:
            self.preencher_alunos(self.alunos)
            return
        filtrados = [
            aluno for aluno in self.alunos
            if any(termo in str(valor).lower() for valor in aluno)
        ]
        self.preencher_alunos(filtrados)

    def selecionar_aluno(self, event=None):
        selecao = self.tabela_alunos.selection()
        if not selecao:
            return

        valores = self.tabela_alunos.item(selecao[0], "values")
        self.id_aluno_selecionado = int(valores[0])
        self.id_nota_selecionada = None

        self.label_id_aluno.config(text=valores[0])
        self.label_nome_aluno.config(text=valores[1])
        self.label_email_aluno.config(text=valores[2])
        self.label_curso_aluno.config(text=valores[3])
        self.recarregar_notas()

    def recarregar_notas(self):
        self.tabela_notas.delete(*self.tabela_notas.get_children())
        self.notas = []

        if self.id_aluno_selecionado is None:
            self.label_titulo_notas.config(text="Notas do aluno selecionado")
            self.label_total_notas.config(text="0 notas")
            return

        aluno = buscar_aluno_por_id(self.id_aluno_selecionado)
        nome = aluno[1] if aluno else f"ID {self.id_aluno_selecionado}"
        self.label_titulo_notas.config(text=f"Notas de {nome}")

        self.notas = listar_notas_por_aluno(self.id_aluno_selecionado)
        for nota in self.notas:
            valores = (nota[0], nota[1], nota[2], nota[3], nota[4], nota[5])
            self.tabela_notas.insert("", "end", iid=str(nota[0]), values=valores)

        total = len(self.notas)
        self.label_total_notas.config(text=f"{total} nota{'s' if total != 1 else ''}")

    def selecionar_nota(self, event=None):
        selecao = self.tabela_notas.selection()
        if not selecao:
            return
        valores = self.tabela_notas.item(selecao[0], "values")
        self.id_nota_selecionada = int(valores[0])

    def atualizar_tudo(self):
        self.recarregar_alunos()
        if self.id_aluno_selecionado is not None:
            self.recarregar_notas()

    def limpar_selecao(self):
        self.id_aluno_selecionado = None
        self.id_nota_selecionada = None
        self.label_id_aluno.config(text="-")
        self.label_nome_aluno.config(text="-")
        self.label_email_aluno.config(text="-")
        self.label_curso_aluno.config(text="-")
        self.tabela_notas.delete(*self.tabela_notas.get_children())
        self.label_titulo_notas.config(text="Notas do aluno selecionado")
        self.label_total_notas.config(text="0 notas")

    def abrir_janela_novo_aluno(self):
        JanelaAluno(self, "Cadastrar aluno")

    def abrir_janela_editar_aluno(self):
        if self.id_aluno_selecionado is None:
            messagebox.showwarning("Selecione um aluno", "Clique em um aluno antes de editar.")
            return
        aluno = buscar_aluno_por_id(self.id_aluno_selecionado)
        if not aluno:
            messagebox.showerror("Erro", "Aluno nao encontrado.")
            return
        JanelaAluno(self, "Editar aluno", aluno)

    def salvar_aluno(self, janela, dados, id_aluno=None):
        nome, email, curso = dados
        if id_aluno is None:
            inserir_aluno(nome, email, curso)
            messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
        else:
            atualizar_aluno(id_aluno, nome, email, curso)
            messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")

        janela.destroy()
        self.recarregar_alunos()
        if id_aluno is not None:
            self.id_aluno_selecionado = id_aluno
            self.selecionar_linha_aluno(id_aluno)

    def selecionar_linha_aluno(self, id_aluno):
        iid = str(id_aluno)
        if iid in self.tabela_alunos.get_children():
            self.tabela_alunos.selection_set(iid)
            self.tabela_alunos.see(iid)
            self.selecionar_aluno()

    def excluir_aluno(self):
        if self.id_aluno_selecionado is None:
            messagebox.showwarning("Selecione um aluno", "Clique em um aluno antes de excluir.")
            return

        nome = self.label_nome_aluno.cget("text")
        confirmado = messagebox.askyesno(
            "Confirmar exclusao",
            f'Deseja excluir o aluno "{nome}" e todas as notas dele?'
        )
        if not confirmado:
            return

        deletar_aluno(self.id_aluno_selecionado)
        messagebox.showinfo("Sucesso", "Aluno excluido com sucesso!")
        self.limpar_selecao()
        self.recarregar_alunos()

    def abrir_janela_nova_nota(self):
        if self.id_aluno_selecionado is None:
            messagebox.showwarning("Selecione um aluno", "Clique em um aluno antes de cadastrar notas.")
            return
        JanelaNota(self, "Cadastrar notas")

    def abrir_janela_editar_nota(self):
        if self.id_nota_selecionada is None:
            messagebox.showwarning("Selecione uma nota", "Clique em uma nota antes de editar.")
            return
        nota = next((nota for nota in self.notas if nota[0] == self.id_nota_selecionada), None)
        if not nota:
            messagebox.showerror("Erro", "Nota nao encontrada.")
            return
        JanelaNota(self, "Editar notas", nota)

    def salvar_nota(self, janela, dados, id_nota=None):
        if self.id_aluno_selecionado is None:
            messagebox.showwarning("Selecione um aluno", "Clique em um aluno antes de salvar notas.")
            return

        disciplina, sm1, sm2, av1, av2 = dados
        if id_nota is None:
            inserir_notas(self.id_aluno_selecionado, disciplina, sm1, sm2, av1, av2)
            messagebox.showinfo("Sucesso", "Notas cadastradas com sucesso!")
        else:
            atualizar_notas(id_nota, disciplina, sm1, sm2, av1, av2)
            messagebox.showinfo("Sucesso", "Notas atualizadas com sucesso!")

        janela.destroy()
        self.recarregar_notas()

    def excluir_nota(self):
        if self.id_nota_selecionada is None:
            messagebox.showwarning("Selecione uma nota", "Clique em uma nota antes de excluir.")
            return

        confirmado = messagebox.askyesno("Confirmar exclusao", "Deseja excluir esta nota?")
        if not confirmado:
            return

        deletar_notas(self.id_nota_selecionada)
        self.id_nota_selecionada = None
        messagebox.showinfo("Sucesso", "Notas excluidas com sucesso!")
        self.recarregar_notas()


class JanelaFormulario(tk.Toplevel):
    def __init__(self, app, titulo, largura=420, altura=360):
        super().__init__(app)
        self.app = app
        self.title(titulo)
        self.configure(bg=BG)
        self.resizable(False, False)
        self.transient(app)
        self.grab_set()
        self.centralizar(largura, altura)

        self.painel = tk.Frame(
            self,
            bg=PANEL,
            highlightthickness=1,
            highlightbackground=BORDER,
        )
        self.painel.pack(fill="both", expand=True, padx=14, pady=14)

        tk.Label(
            self.painel,
            text=titulo,
            font=FONT_HEAD,
            bg=PANEL,
            fg=TEXT,
        ).pack(anchor="w", padx=18, pady=(16, 10))

    def centralizar(self, largura, altura):
        self.update_idletasks()
        x = self.app.winfo_x() + (self.app.winfo_width() - largura) // 2
        y = self.app.winfo_y() + (self.app.winfo_height() - altura) // 2
        self.geometry(f"{largura}x{altura}+{x}+{y}")

    def criar_campo(self, label, valor=""):
        tk.Label(
            self.painel,
            text=label,
            font=FONT_SMALL,
            bg=PANEL,
            fg=MUTED,
        ).pack(anchor="w", padx=18, pady=(8, 1))

        variavel = tk.StringVar(value=valor)
        entrada = tk.Entry(
            self.painel,
            textvariable=variavel,
            font=FONT_BODY,
            bg=ENTRY_BG,
            fg=TEXT,
            insertbackground=ACCENT,
            relief="flat",
            bd=8,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
        )
        entrada.pack(fill="x", padx=18)
        return variavel

    def criar_botoes(self, texto_salvar, comando_salvar):
        linha = tk.Frame(self.painel, bg=PANEL)
        linha.pack(fill="x", padx=18, pady=(18, 0))

        tk.Button(
            linha,
            text=texto_salvar,
            command=comando_salvar,
            font=FONT_BODY,
            bg=SUCCESS,
            fg=TEXT,
            activebackground=ACCENT2,
            activeforeground="white",
            relief="flat",
            bd=0,
            pady=8,
            cursor="hand2",
        ).pack(side="left", fill="x", expand=True, padx=(0, 6))

        tk.Button(
            linha,
            text="Cancelar",
            command=self.destroy,
            font=FONT_BODY,
            bg=PANEL,
            fg=TEXT,
            activebackground=ACCENT2,
            activeforeground="white",
            relief="flat",
            bd=0,
            pady=8,
            cursor="hand2",
            highlightthickness=1,
            highlightbackground=BORDER,
        ).pack(side="left", fill="x", expand=True, padx=(6, 0))


class JanelaAluno(JanelaFormulario):
    def __init__(self, app, titulo, aluno=None):
        super().__init__(app, titulo, 430, 390)
        self.aluno = aluno

        id_texto = str(aluno[0]) if aluno else "Gerado automaticamente"
        tk.Label(
            self.painel,
            text=f"ID: {id_texto}",
            font=FONT_MONO,
            bg=PANEL,
            fg=ACCENT,
        ).pack(anchor="w", padx=18, pady=(0, 6))

        self.nome = self.criar_campo("Nome", aluno[1] if aluno else "")
        self.email = self.criar_campo("Email", aluno[2] if aluno else "")
        self.curso = self.criar_campo("Curso", aluno[3] if aluno else "")
        self.criar_botoes("Salvar aluno", self.salvar)

    def salvar(self):
        nome = self.nome.get().strip()
        email = self.email.get().strip()
        curso = self.curso.get().strip()

        if not nome:
            messagebox.showerror("Erro", "Informe o nome do aluno.")
            return
        if not email:
            messagebox.showerror("Erro", "Informe o email do aluno.")
            return
        if not curso:
            messagebox.showerror("Erro", "Informe o curso do aluno.")
            return

        id_aluno = self.aluno[0] if self.aluno else None
        self.app.salvar_aluno(self, (nome, email, curso), id_aluno)


class JanelaNota(JanelaFormulario):
    def __init__(self, app, titulo, nota=None):
        super().__init__(app, titulo, 430, 500)
        self.nota = nota

        aluno = buscar_aluno_por_id(app.id_aluno_selecionado)
        nome_aluno = aluno[1] if aluno else "Aluno selecionado"
        tk.Label(
            self.painel,
            text=f"Aluno: {nome_aluno}",
            font=FONT_MONO,
            bg=PANEL,
            fg=ACCENT,
            wraplength=360,
            justify="left",
        ).pack(anchor="w", padx=18, pady=(0, 6))

        self.disciplina = self.criar_campo("Disciplina", nota[1] if nota else "")
        self.sm1 = self.criar_campo("Simulado 1", nota[2] if nota else "")
        self.sm2 = self.criar_campo("Simulado 2", nota[3] if nota else "")
        self.av1 = self.criar_campo("Avaliacao 1", nota[4] if nota else "")
        self.av2 = self.criar_campo("Avaliacao 2", nota[5] if nota else "")
        self.criar_botoes("Salvar notas", self.salvar)

    def converter_numero(self, variavel, nome_campo):
        texto = str(variavel.get()).strip().replace(",", ".")
        try:
            return float(texto)
        except ValueError:
            messagebox.showerror("Erro", f"O campo {nome_campo} deve conter apenas numeros.")
            return None

    def salvar(self):
        disciplina = self.disciplina.get().strip()
        if not disciplina:
            messagebox.showerror("Erro", "Informe a disciplina.")
            return

        sm1 = self.converter_numero(self.sm1, "Simulado 1")
        sm2 = self.converter_numero(self.sm2, "Simulado 2")
        av1 = self.converter_numero(self.av1, "Avaliacao 1")
        av2 = self.converter_numero(self.av2, "Avaliacao 2")

        if sm1 is None or sm2 is None or av1 is None or av2 is None:
            return

        id_nota = self.nota[0] if self.nota else None
        self.app.salvar_nota(self, (disciplina, sm1, sm2, av1, av2), id_nota)


if __name__ == "__main__":
    app = App()
    app.mainloop()
