import sqlite3

conn = sqlite3.connect('banco.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS usuarios;')

# Estrutura conforme o quadro da Aula 1 (13/08)
cursor.execute('''
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER
);
''')

cursor.execute("INSERT INTO usuarios (name, age) VALUES ('Carlos', 25);")
cursor.execute("INSERT INTO usuarios (name, age) VALUES ('Ana', 30);")
conn.commit()

# 3. READ (Consultando os dados inseridos)
cursor.execute("SELECT * FROM usuarios;")
print("=== CONSULTA INICIAL (READ) ===")
print(cursor.fetchall())

# 4. UPDATE (Atualizando a idade do Carlos)
cursor.execute("UPDATE usuarios SET age = 26 WHERE name = 'Carlos';")
conn.commit()

# 5. DELETE (Removendo a Ana)
cursor.execute("DELETE FROM usuarios WHERE name = 'Ana';")
conn.commit()

# Consulta final para verificar o resultado das alterações
cursor.execute("SELECT * FROM usuarios;")
print("=== APÓS UPDATE E DELETE ===")
print(cursor.fetchall())

conn.close()