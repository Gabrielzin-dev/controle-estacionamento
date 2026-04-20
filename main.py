import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from database import (
    inicializar_banco,
    listar_clientes,
    cadastrar_cliente,
    atualizar_cliente,
    excluir_cliente,
    registrar_entrada,
    registrar_saida,
    listar_movimentacoes,
    listar_movimentacoes_em_aberto,
    listar_financeiro,
    baixar_pagamento,
    relatorio_clientes,
    relatorio_recebimentos_em_aberto,
    relatorio_recebimentos_pagos,
    relatorio_top5_clientes,
    obter_vagas_ocupadas,
    obter_vagas_livres,
    TOTAL_VAGAS,
    VALOR_HORA
)


class SistemaEstacionamento:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Controle de Estacionamento")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)

        self.cliente_selecionado_id = None
        self.financeiro_selecionado_id = None

        self.criar_interface()
        self.atualizar_tudo()

    def criar_interface(self):
        topo = tk.Frame(self.root, pady=10)
        topo.pack(fill="x")

        self.lbl_resumo = tk.Label(
            topo,
            text="",
            font=("Arial", 12, "bold")
        )
        self.lbl_resumo.pack()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.aba_clientes = ttk.Frame(self.notebook)
        self.aba_movimentacao = ttk.Frame(self.notebook)
        self.aba_financeiro = ttk.Frame(self.notebook)
        self.aba_relatorios = ttk.Frame(self.notebook)

        self.notebook.add(self.aba_clientes, text="Clientes")
        self.notebook.add(self.aba_movimentacao, text="Movimentação")
        self.notebook.add(self.aba_financeiro, text="Financeiro")
        self.notebook.add(self.aba_relatorios, text="Relatórios")

        self.criar_aba_clientes()
        self.criar_aba_movimentacao()
        self.criar_aba_financeiro()
        self.criar_aba_relatorios()

    # =========================
    # ABA CLIENTES
    # =========================
    def criar_aba_clientes(self):
        frame_form = tk.LabelFrame(self.aba_clientes, text="Cadastro de Clientes", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_form, text="Nome", width=10, anchor="w").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome = tk.Entry(frame_form, width=40)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        tk.Label(frame_form, text="CPF", width=10, anchor="w").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_cpf = tk.Entry(frame_form, width=25)
        self.entry_cpf.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        tk.Label(frame_form, text="Placa", width=10, anchor="w").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_placa = tk.Entry(frame_form, width=20)
        self.entry_placa.grid(row=2, column=1, padx=5, pady=5, sticky="we")

        frame_botoes = tk.Frame(frame_form)
        frame_botoes.grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(frame_botoes, text="Cadastrar", width=15, command=self.salvar_cliente).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Atualizar", width=15, command=self.editar_cliente).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Excluir", width=15, command=self.remover_cliente).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Limpar", width=15, command=self.limpar_form_cliente).pack(side="left", padx=5)

        frame_lista = tk.LabelFrame(self.aba_clientes, text="Clientes Cadastrados", padx=10, pady=10)
        frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

        colunas = ("id", "nome", "cpf", "placa")
        self.tree_clientes = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=15)

        self.tree_clientes.heading("id", text="ID")
        self.tree_clientes.heading("nome", text="Nome")
        self.tree_clientes.heading("cpf", text="CPF")
        self.tree_clientes.heading("placa", text="Placa")

        self.tree_clientes.column("id", width=60, anchor="center")
        self.tree_clientes.column("nome", width=400)
        self.tree_clientes.column("cpf", width=200, anchor="center")
        self.tree_clientes.column("placa", width=150, anchor="center")

        self.tree_clientes.pack(fill="both", expand=True)
        self.tree_clientes.bind("<<TreeviewSelect>>", self.selecionar_cliente)

    def salvar_cliente(self):
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        placa = self.entry_placa.get().strip().upper()

        if not nome or not cpf or not placa:
            messagebox.showwarning("Atenção", "Preencha nome, CPF e placa.")
            return

        try:
            cadastrar_cliente(nome, cpf, placa)
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso.")
            self.limpar_form_cliente()
            self.atualizar_tudo()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "CPF ou placa já cadastrados.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def editar_cliente(self):
        if not self.cliente_selecionado_id:
            messagebox.showwarning("Atenção", "Selecione um cliente para atualizar.")
            return

        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        placa = self.entry_placa.get().strip().upper()

        if not nome or not cpf or not placa:
            messagebox.showwarning("Atenção", "Preencha nome, CPF e placa.")
            return

        try:
            atualizar_cliente(self.cliente_selecionado_id, nome, cpf, placa)
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso.")
            self.limpar_form_cliente()
            self.atualizar_tudo()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "CPF ou placa já cadastrados em outro registro.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def remover_cliente(self):
        if not self.cliente_selecionado_id:
            messagebox.showwarning("Atenção", "Selecione um cliente para excluir.")
            return

        confirmar = messagebox.askyesno("Confirmar", "Deseja realmente excluir este cliente?")
        if not confirmar:
            return

        try:
            excluir_cliente(self.cliente_selecionado_id)
            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso.")
            self.limpar_form_cliente()
            self.atualizar_tudo()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def selecionar_cliente(self, event):
        selecionado = self.tree_clientes.selection()
        if not selecionado:
            return

        valores = self.tree_clientes.item(selecionado[0], "values")
        self.cliente_selecionado_id = valores[0]

        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, valores[1])

        self.entry_cpf.delete(0, tk.END)
        self.entry_cpf.insert(0, valores[2])

        self.entry_placa.delete(0, tk.END)
        self.entry_placa.insert(0, valores[3])

    def limpar_form_cliente(self):
        self.cliente_selecionado_id = None
        self.entry_nome.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)
        self.entry_placa.delete(0, tk.END)

    def atualizar_tree_clientes(self):
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)

        for cliente in listar_clientes():
            self.tree_clientes.insert("", tk.END, values=cliente)

    # =========================
    # ABA MOVIMENTAÇÃO
    # =========================
    def criar_aba_movimentacao(self):
        frame_controle = tk.LabelFrame(self.aba_movimentacao, text="Registro de Utilização das Vagas", padx=10, pady=10)
        frame_controle.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_controle, text="Placa do veículo").grid(row=0, column=0, padx=5, pady=5)
        self.entry_placa_mov = tk.Entry(frame_controle, width=20)
        self.entry_placa_mov.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(frame_controle, text="Registrar Entrada", width=18, command=self.acao_registrar_entrada).grid(row=0, column=2, padx=5)
        tk.Button(frame_controle, text="Registrar Saída", width=18, command=self.acao_registrar_saida).grid(row=0, column=3, padx=5)

        frame_lista = tk.LabelFrame(self.aba_movimentacao, text="Movimentações", padx=10, pady=10)
        frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

        colunas = ("id", "nome", "cpf", "placa", "data", "entrada", "saida", "valor", "status")
        self.tree_movimentacao = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=18)

        titulos = {
            "id": "ID",
            "nome": "Nome",
            "cpf": "CPF",
            "placa": "Placa",
            "data": "Data",
            "entrada": "Hora Entrada",
            "saida": "Hora Saída",
            "valor": "Valor",
            "status": "Pagamento"
        }

        larguras = {
            "id": 60,
            "nome": 220,
            "cpf": 130,
            "placa": 100,
            "data": 100,
            "entrada": 100,
            "saida": 100,
            "valor": 100,
            "status": 120
        }

        for col in colunas:
            self.tree_movimentacao.heading(col, text=titulos[col])
            self.tree_movimentacao.column(col, width=larguras[col], anchor="center")

        self.tree_movimentacao.pack(fill="both", expand=True)

        frame_abertas = tk.LabelFrame(self.aba_movimentacao, text="Entradas em Aberto", padx=10, pady=10)
        frame_abertas.pack(fill="both", expand=False, padx=10, pady=10)

        colunas_abertas = ("id", "nome", "placa", "data", "entrada")
        self.tree_abertas = ttk.Treeview(frame_abertas, columns=colunas_abertas, show="headings", height=6)

        for col, texto, largura in [
            ("id", "ID", 60),
            ("nome", "Nome", 250),
            ("placa", "Placa", 120),
            ("data", "Data", 120),
            ("entrada", "Hora Entrada", 120),
        ]:
            self.tree_abertas.heading(col, text=texto)
            self.tree_abertas.column(col, width=largura, anchor="center")

        self.tree_abertas.pack(fill="both", expand=True)

    def acao_registrar_entrada(self):
        placa = self.entry_placa_mov.get().strip().upper()
        if not placa:
            messagebox.showwarning("Atenção", "Digite a placa.")
            return

        try:
            registrar_entrada(placa)
            messagebox.showinfo("Sucesso", "Entrada registrada com sucesso.")
            self.entry_placa_mov.delete(0, tk.END)
            self.atualizar_tudo()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def acao_registrar_saida(self):
        placa = self.entry_placa_mov.get().strip().upper()
        if not placa:
            messagebox.showwarning("Atenção", "Digite a placa.")
            return

        try:
            registrar_saida(placa)
            messagebox.showinfo("Sucesso", "Saída registrada com sucesso.")
            self.entry_placa_mov.delete(0, tk.END)
            self.atualizar_tudo()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar_tree_movimentacao(self):
        for item in self.tree_movimentacao.get_children():
            self.tree_movimentacao.delete(item)

        for mov in listar_movimentacoes():
            mov = list(mov)
            mov[7] = f"R$ {float(mov[7]):.2f}"
            self.tree_movimentacao.insert("", tk.END, values=mov)

        for item in self.tree_abertas.get_children():
            self.tree_abertas.delete(item)

        for mov_aberta in listar_movimentacoes_em_aberto():
            self.tree_abertas.insert("", tk.END, values=mov_aberta)

    # =========================
    # ABA FINANCEIRO
    # =========================
    def criar_aba_financeiro(self):
        frame_info = tk.LabelFrame(self.aba_financeiro, text="Financeiro", padx=10, pady=10)
        frame_info.pack(fill="x", padx=10, pady=10)

        self.lbl_financeiro = tk.Label(
            frame_info,
            text=f"Valor por hora: R$ {VALOR_HORA:.2f}",
            font=("Arial", 11, "bold")
        )
        self.lbl_financeiro.pack(anchor="w")

        frame_lista = tk.LabelFrame(self.aba_financeiro, text="Movimentações Finalizadas", padx=10, pady=10)
        frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

        colunas = ("id", "nome", "placa", "data", "entrada", "saida", "valor", "status")
        self.tree_financeiro = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=18)

        for col, texto, largura in [
            ("id", "ID", 60),
            ("nome", "Nome", 250),
            ("placa", "Placa", 100),
            ("data", "Data", 100),
            ("entrada", "Hora Entrada", 100),
            ("saida", "Hora Saída", 100),
            ("valor", "Valor", 100),
            ("status", "Status", 120),
        ]:
            self.tree_financeiro.heading(col, text=texto)
            self.tree_financeiro.column(col, width=largura, anchor="center")

        self.tree_financeiro.pack(fill="both", expand=True)
        self.tree_financeiro.bind("<<TreeviewSelect>>", self.selecionar_financeiro)

        frame_botoes = tk.Frame(self.aba_financeiro)
        frame_botoes.pack(pady=10)

        tk.Button(frame_botoes, text="Dar baixa no pagamento", width=25, command=self.acao_baixar_pagamento).pack()

    def selecionar_financeiro(self, event):
        selecionado = self.tree_financeiro.selection()
        if not selecionado:
            return

        valores = self.tree_financeiro.item(selecionado[0], "values")
        self.financeiro_selecionado_id = valores[0]

    def acao_baixar_pagamento(self):
        if not self.financeiro_selecionado_id:
            messagebox.showwarning("Atenção", "Selecione uma movimentação finalizada.")
            return

        try:
            baixar_pagamento(self.financeiro_selecionado_id)
            messagebox.showinfo("Sucesso", "Pagamento baixado com sucesso.")
            self.financeiro_selecionado_id = None
            self.atualizar_tudo()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar_tree_financeiro(self):
        for item in self.tree_financeiro.get_children():
            self.tree_financeiro.delete(item)

        for fin in listar_financeiro():
            fin = list(fin)
            fin[6] = f"R$ {float(fin[6]):.2f}"
            self.tree_financeiro.insert("", tk.END, values=fin)

    # =========================
    # ABA RELATÓRIOS
    # =========================
    def criar_aba_relatorios(self):
        frame_botoes = tk.LabelFrame(self.aba_relatorios, text="Relatórios Disponíveis", padx=10, pady=10)
        frame_botoes.pack(fill="x", padx=10, pady=10)

        tk.Button(frame_botoes, text="Relatório de Clientes", width=25, command=self.mostrar_relatorio_clientes).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(frame_botoes, text="Recebimentos em Aberto", width=25, command=self.mostrar_relatorio_abertos).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame_botoes, text="Recebimentos Pagos", width=25, command=self.mostrar_relatorio_pagos).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(frame_botoes, text="Top 5 Clientes", width=25, command=self.mostrar_relatorio_top5).grid(row=0, column=3, padx=5, pady=5)

        frame_tabela = tk.LabelFrame(self.aba_relatorios, text="Visualização", padx=10, pady=10)
        frame_tabela.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_relatorios = ttk.Treeview(frame_tabela, show="headings")
        self.tree_relatorios.pack(fill="both", expand=True)

    def configurar_tree_relatorio(self, colunas, titulos, larguras):
        self.tree_relatorios.delete(*self.tree_relatorios.get_children())

        self.tree_relatorios["columns"] = colunas
        for col in self.tree_relatorios["columns"]:
            self.tree_relatorios.heading(col, text=titulos[col])
            self.tree_relatorios.column(col, width=larguras[col], anchor="center")

    def mostrar_relatorio_clientes(self):
        colunas = ("id", "nome", "cpf", "placa")
        titulos = {
            "id": "ID",
            "nome": "Nome",
            "cpf": "CPF",
            "placa": "Placa"
        }
        larguras = {"id": 80, "nome": 350, "cpf": 200, "placa": 150}

        self.configurar_tree_relatorio(colunas, titulos, larguras)

        for linha in relatorio_clientes():
            self.tree_relatorios.insert("", tk.END, values=linha)

    def mostrar_relatorio_abertos(self):
        colunas = ("id", "nome", "placa", "data", "entrada", "saida", "valor")
        titulos = {
            "id": "ID",
            "nome": "Nome",
            "placa": "Placa",
            "data": "Data",
            "entrada": "Hora Entrada",
            "saida": "Hora Saída",
            "valor": "Valor"
        }
        larguras = {"id": 70, "nome": 250, "placa": 120, "data": 100, "entrada": 100, "saida": 100, "valor": 100}

        self.configurar_tree_relatorio(colunas, titulos, larguras)

        for linha in relatorio_recebimentos_em_aberto():
            linha = list(linha)
            linha[6] = f"R$ {float(linha[6]):.2f}"
            self.tree_relatorios.insert("", tk.END, values=linha)

    def mostrar_relatorio_pagos(self):
        colunas = ("id", "nome", "placa", "data", "entrada", "saida", "valor")
        titulos = {
            "id": "ID",
            "nome": "Nome",
            "placa": "Placa",
            "data": "Data",
            "entrada": "Hora Entrada",
            "saida": "Hora Saída",
            "valor": "Valor"
        }
        larguras = {"id": 70, "nome": 250, "placa": 120, "data": 100, "entrada": 100, "saida": 100, "valor": 100}

        self.configurar_tree_relatorio(colunas, titulos, larguras)

        for linha in relatorio_recebimentos_pagos():
            linha = list(linha)
            linha[6] = f"R$ {float(linha[6]):.2f}"
            self.tree_relatorios.insert("", tk.END, values=linha)

    def mostrar_relatorio_top5(self):
        colunas = ("nome", "placa", "total_usos")
        titulos = {
            "nome": "Nome",
            "placa": "Placa",
            "total_usos": "Quantidade de usos"
        }
        larguras = {"nome": 350, "placa": 180, "total_usos": 180}

        self.configurar_tree_relatorio(colunas, titulos, larguras)

        for linha in relatorio_top5_clientes():
            self.tree_relatorios.insert("", tk.END, values=linha)

    # =========================
    # ATUALIZAÇÕES GERAIS
    # =========================
    def atualizar_resumo_vagas(self):
        ocupadas = obter_vagas_ocupadas()
        livres = obter_vagas_livres()

        self.lbl_resumo.config(
            text=(
                f"Total de vagas: {TOTAL_VAGAS} | "
                f"Ocupadas: {ocupadas} | "
                f"Livres: {livres} | "
                f"Valor por hora: R$ {VALOR_HORA:.2f}"
            )
        )

    def atualizar_tudo(self):
        self.atualizar_resumo_vagas()
        self.atualizar_tree_clientes()
        self.atualizar_tree_movimentacao()
        self.atualizar_tree_financeiro()


if __name__ == "__main__":
    inicializar_banco()
    root = tk.Tk()
    app = SistemaEstacionamento(root)
    root.mainloop()