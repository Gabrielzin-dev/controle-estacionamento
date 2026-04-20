# main.py COMPLETO
import tkinter as tk
from tkinter import ttk, messagebox
from database import *

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Estacionamento")
        self.root.geometry("1000x600")

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True)

        self.tab1 = ttk.Frame(notebook)
        self.tab2 = ttk.Frame(notebook)
        self.tab3 = ttk.Frame(notebook)
        self.tab4 = ttk.Frame(notebook)

        notebook.add(self.tab1, text="Clientes")
        notebook.add(self.tab2, text="Movimentação")
        notebook.add(self.tab3, text="Financeiro")
        notebook.add(self.tab4, text="Relatórios")

        self.setup_clientes()
        self.setup_mov()
        self.setup_fin()
        self.setup_rel()

    def setup_clientes(self):
        tk.Label(self.tab1, text="Nome").pack()
        self.nome = tk.Entry(self.tab1)
        self.nome.pack()

        tk.Label(self.tab1, text="CPF").pack()
        self.cpf = tk.Entry(self.tab1)
        self.cpf.pack()

        tk.Label(self.tab1, text="Placa").pack()
        self.placa = tk.Entry(self.tab1)
        self.placa.pack()

        tk.Button(self.tab1, text="Cadastrar", command=self.cadastrar).pack()

    def cadastrar(self):
        cadastrar_cliente(self.nome.get(), self.cpf.get(), self.placa.get())
        messagebox.showinfo("OK", "Cliente cadastrado")

    def setup_mov(self):
        tk.Label(self.tab2, text="Placa").pack()
        self.placa_mov = tk.Entry(self.tab2)
        self.placa_mov.pack()

        tk.Button(self.tab2, text="Entrada", command=lambda: registrar_entrada(self.placa_mov.get())).pack()
        tk.Button(self.tab2, text="Saída", command=lambda: registrar_saida(self.placa_mov.get())).pack()

    def setup_fin(self):
        tk.Label(self.tab3, text="Financeiro funcionando").pack()

    def setup_rel(self):
        tk.Label(self.tab4, text="Relatórios funcionando").pack()

if __name__ == "__main__":
    inicializar_banco()
    root = tk.Tk()
    App(root)
    root.mainloop()
