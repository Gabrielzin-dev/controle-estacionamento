import sqlite3
from datetime import datetime
from math import ceil

DB_NAME = "estacionamento.db"
VALOR_HORA = 8.0
TOTAL_VAGAS = 20


def conectar():
    return sqlite3.connect(DB_NAME)


def inicializar_banco():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            placa TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            data_movimentacao TEXT NOT NULL,
            hora_entrada TEXT NOT NULL,
            hora_saida TEXT,
            valor REAL DEFAULT 0,
            pago INTEGER DEFAULT 0,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    """)

    conn.commit()
    conn.close()


# =========================
# CLIENTES
# =========================
def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, cpf, placa
        FROM clientes
        ORDER BY nome
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados


def cadastrar_cliente(nome, cpf, placa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes (nome, cpf, placa)
        VALUES (?, ?, ?)
    """, (nome.strip(), cpf.strip(), placa.strip().upper()))
    conn.commit()
    conn.close()


def atualizar_cliente(cliente_id, nome, cpf, placa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clientes
        SET nome = ?, cpf = ?, placa = ?
        WHERE id = ?
    """, (nome.strip(), cpf.strip(), placa.strip().upper(), cliente_id))
    conn.commit()
    conn.close()


def excluir_cliente(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    conn.commit()
    conn.close()


def buscar_cliente_por_placa(placa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, cpf, placa
        FROM clientes
        WHERE UPPER(placa) = ?
    """, (placa.strip().upper(),))
    dado = cursor.fetchone()
    conn.close()
    return dado


# =========================
# MOVIMENTAÇÃO
# =========================
def veiculo_esta_no_estacionamento(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id
        FROM movimentacoes
        WHERE cliente_id = ? AND hora_saida IS NULL
    """, (cliente_id,))
    dado = cursor.fetchone()
    conn.close()
    return dado is not None


def registrar_entrada(placa):
    cliente = buscar_cliente_por_placa(placa)
    if not cliente:
        raise ValueError("Nenhum cliente encontrado com essa placa.")

    cliente_id = cliente[0]

    if veiculo_esta_no_estacionamento(cliente_id):
        raise ValueError("Este veículo já está com entrada registrada e sem saída.")

    vagas_livres = obter_vagas_livres()
    if vagas_livres <= 0:
        raise ValueError("Não há vagas disponíveis no momento.")

    agora = datetime.now()
    data_mov = agora.strftime("%d/%m/%Y")
    hora_entrada = agora.strftime("%H:%M:%S")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO movimentacoes (cliente_id, data_movimentacao, hora_entrada)
        VALUES (?, ?, ?)
    """, (cliente_id, data_mov, hora_entrada))
    conn.commit()
    conn.close()


def calcular_valor(hora_entrada_str, hora_saida_str):
    entrada = datetime.strptime(hora_entrada_str, "%H:%M:%S")
    saida = datetime.strptime(hora_saida_str, "%H:%M:%S")

    diferenca_horas = (saida - entrada).total_seconds() / 3600

    if diferenca_horas <= 0:
        diferenca_horas = 1

    horas_cobradas = ceil(diferenca_horas)
    return round(horas_cobradas * VALOR_HORA, 2)


def registrar_saida(placa):
    cliente = buscar_cliente_por_placa(placa)
    if not cliente:
        raise ValueError("Nenhum cliente encontrado com essa placa.")

    cliente_id = cliente[0]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, data_movimentacao, hora_entrada
        FROM movimentacoes
        WHERE cliente_id = ? AND hora_saida IS NULL
        ORDER BY id DESC
        LIMIT 1
    """, (cliente_id,))
    movimentacao = cursor.fetchone()

    if not movimentacao:
        conn.close()
        raise ValueError("Não existe entrada em aberto para essa placa.")

    mov_id, _, hora_entrada = movimentacao
    agora = datetime.now()
    hora_saida = agora.strftime("%H:%M:%S")

    valor = calcular_valor(hora_entrada, hora_saida)

    cursor.execute("""
        UPDATE movimentacoes
        SET hora_saida = ?, valor = ?
        WHERE id = ?
    """, (hora_saida, valor, mov_id))

    conn.commit()
    conn.close()


def listar_movimentacoes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            m.id,
            c.nome,
            c.cpf,
            c.placa,
            m.data_movimentacao,
            m.hora_entrada,
            COALESCE(m.hora_saida, '-'),
            m.valor,
            CASE WHEN m.pago = 1 THEN 'Pago' ELSE 'Em aberto' END
        FROM movimentacoes m
        INNER JOIN clientes c ON c.id = m.cliente_id
        ORDER BY m.id DESC
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados


def listar_movimentacoes_em_aberto():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            m.id,
            c.nome,
            c.placa,
            m.data_movimentacao,
            m.hora_entrada
        FROM movimentacoes m
        INNER JOIN clientes c ON c.id = m.cliente_id
        WHERE m.hora_saida IS NULL
        ORDER BY m.id DESC
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados


# =========================
# FINANCEIRO
# =========================
def listar_financeiro():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            m.id,
            c.nome,
            c.placa,
            m.data_movimentacao,
            m.hora_entrada,
            m.hora_saida,
            m.valor,
            CASE WHEN m.pago = 1 THEN 'Pago' ELSE 'Em aberto' END
        FROM movimentacoes m
        INNER JOIN clientes c ON c.id = m.cliente_id
        WHERE m.hora_saida IS NOT NULL
        ORDER BY m.id DESC
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados


def baixar_pagamento(movimentacao_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE movimentacoes
        SET pago = 1
        WHERE id = ?
    """, (movimentacao_id,))
    conn.commit()
    conn.close()


# =========================
# RELATÓRIOS
# =========================
def relatorio_clientes():
    return listar_clientes()


def relatorio_recebimentos_em_aberto():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            m.id,
            c.nome,
            c.placa,
            m.data_movimentacao,
            m.hora_entrada,
            m.hora_saida,
            m.valor
        FROM movimentacoes m
        INNER JOIN clientes c ON c.id = m.cliente_id
        WHERE m.hora_saida IS NOT NULL AND m.pago = 0
        ORDER BY m.id DESC
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados


def relatorio_recebimentos_pagos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            m.id,
            c.nome,
            c.placa,
            m.data_movimentacao,
            m.hora_entrada,
            m.hora_saida,
            m.valor
        FROM movimentacoes m
        INNER JOIN clientes c ON c.id = m.cliente_id
        WHERE m.hora_saida IS NOT NULL AND m.pago = 1
        ORDER BY m.id DESC
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados


def relatorio_top5_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            c.nome,
            c.placa,
            COUNT(m.id) AS total_usos
        FROM clientes c
        INNER JOIN movimentacoes m ON m.cliente_id = c.id
        GROUP BY c.id, c.nome, c.placa
        ORDER BY total_usos DESC, c.nome ASC
        LIMIT 5
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados


# =========================
# VAGAS
# =========================
def obter_vagas_ocupadas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM movimentacoes
        WHERE hora_saida IS NULL
    """)
    ocupadas = cursor.fetchone()[0]
    conn.close()
    return ocupadas


def obter_vagas_livres():
    return TOTAL_VAGAS - obter_vagas_ocupadas()