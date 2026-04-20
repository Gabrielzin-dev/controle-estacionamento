# database.py COMPLETO
import sqlite3
from datetime import datetime
from math import ceil

def conectar():
    return sqlite3.connect("estacionamento.db")

def inicializar_banco():
    conn = conectar()
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS clientes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        cpf TEXT,
        placa TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS movimentacoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT,
        entrada TEXT,
        saida TEXT,
        valor REAL,
        pago INTEGER DEFAULT 0
    )""")

    conn.commit()
    conn.close()

def cadastrar_cliente(nome, cpf, placa):
    conn = conectar()
    c = conn.cursor()
    c.execute("INSERT INTO clientes(nome,cpf,placa) VALUES (?,?,?)",(nome,cpf,placa))
    conn.commit()
    conn.close()

def registrar_entrada(placa):
    conn = conectar()
    c = conn.cursor()
    c.execute("INSERT INTO movimentacoes(placa,entrada) VALUES (?,datetime('now'))",(placa,))
    conn.commit()
    conn.close()

def registrar_saida(placa):
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT id,entrada FROM movimentacoes WHERE placa=? AND saida IS NULL",(placa,))
    r = c.fetchone()
    if r:
        from datetime import datetime
        entrada = datetime.fromisoformat(r[1])
        saida = datetime.now()
        horas = ceil((saida-entrada).seconds/3600)
        valor = horas*10
        c.execute("UPDATE movimentacoes SET saida=datetime('now'),valor=? WHERE id=?",(valor,r[0]))
        conn.commit()
    conn.close()
