import sqlite3

conn = sqlite3.connect('aula1.db')
cursor = conn.cursor()

cursor.execute('PRAGMA foreign_keys = ON;')

cursor.execute('DROP TABLE IF EXISTS pedidos;')
cursor.execute('DROP TABLE IF EXISTS clientes;')

cursor.execute('''
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    valor REAL,
    status TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);
''')

cursor.execute("INSERT INTO clientes (nome) VALUES ('Alice'), ('Bruno'), ('Carla');")
cursor.execute("INSERT INTO pedidos (cliente_id, valor, status) VALUES (1, 150.0, 'Concluido');")
cursor.execute("INSERT INTO pedidos (cliente_id, valor, status) VALUES (1, 300.0, 'Concluido');")
cursor.execute("INSERT INTO pedidos (cliente_id, valor, status) VALUES (2, 50.0, 'Pendente');")
cursor.execute("INSERT INTO pedidos (cliente_id, valor, status) VALUES (3, 500.0, 'Concluido');")
conn.commit()

# --- CONSULTAS DA AULA 1 ---

# Exemplo 1: Filtro com WHERE (pega so os pedidos concluidos)
print("=== Pedidos Concluidos ===")
cursor.execute("SELECT * FROM pedidos WHERE status = 'Concluido';")
print(cursor.fetchall())

# Exemplo 2: Usando JOIN para juntar o nome do cliente com o valor do pedido
print("\n=== Cliente e Valor ===")
cursor.execute('''
SELECT clientes.nome, pedidos.valor 
FROM pedidos 
INNER JOIN clientes ON pedidos.cliente_id = clientes.id;
''')
print(cursor.fetchall())

# Exemplo 3: GROUP BY e HAVING (soma o total por cliente e filtra os maiores que 200)
print("\n=== Clientes que gastaram mais de 200 ===")
cursor.execute('''
SELECT cliente_id, SUM(valor) 
FROM pedidos 
GROUP BY cliente_id 
HAVING SUM(valor) > 200.0;
''')
print(cursor.fetchall())

conn.close()