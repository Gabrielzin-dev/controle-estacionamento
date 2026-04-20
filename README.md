# Sistema de Controle de Estacionamento

Aplicativo desenvolvido em Python para controle de vagas em um estacionamento, com cadastro de clientes, movimentação de veículos, controle financeiro e relatórios.

## Objetivo

O projeto foi desenvolvido para atender ao enunciado da disciplina de ADS, aplicando conceitos de programação, interface gráfica, banco de dados e organização de sistema.

## Tecnologias utilizadas

- Python
- Tkinter
- SQLite

## Funcionalidades

### Cadastro de clientes
<img width="1497" height="906" alt="image" src="https://github.com/user-attachments/assets/66eec040-5b0c-438c-a2f7-4acf79756fea" />

O sistema possui CRUD completo de clientes, permitindo:
- cadastrar clientes
- atualizar clientes
- excluir clientes
- listar clientes

Campos cadastrados:
- Nome
- CPF
- Placa do veículo

### Movimentação
<img width="1488" height="906" alt="image" src="https://github.com/user-attachments/assets/ae493226-ff55-4c91-94d4-76e066baadbd" />

O sistema possui uma aba de movimentação para registrar a utilização das vagas, contendo:
- Data
- Hora de entrada
- Hora de saída
- Placa

Também faz o controle de:
- vagas ocupadas
- vagas livres
- impedimento de dupla entrada sem saída

### Financeiro
<img width="1489" height="900" alt="image" src="https://github.com/user-attachments/assets/e437c2c3-dbcf-453f-b791-886cbb642c39" />

O sistema possui uma aba financeira com:
- cálculo automático do valor a receber
- valor por hora configurado no sistema
- controle de pagamentos
- baixa de pagamento

### Relatórios
<img width="1488" height="889" alt="image" src="https://github.com/user-attachments/assets/cbfb7c07-1a71-4af9-aadd-d667f4552d01" />

O sistema possui os seguintes relatórios:
- Clientes
- Recebimentos em aberto
- Recebimentos pagos
- Top 5 clientes que mais utilizaram o estacionamento

## Estrutura do projeto

```bash
controle-estacionamento/
│
├── main.py
├── database.py
├── README.md
├── requirements.txt
├── .gitignore
└── uml/
    ├── diagrama_classes.puml
    ├── diagrama_componentes.puml
    └── diagrama_caso_de_uso.puml
