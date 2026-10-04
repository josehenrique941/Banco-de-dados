import sqlite3

conn = sqlite3.connect('aula2.db')
cursor = conn.cursor()

cursor.execute('PRAGMA foreign_keys = ON;')

cursor.execute('DROP TABLE IF EXISTS city;')
cursor.execute('DROP TABLE IF EXISTS country;')


cursor.execute('''
CREATE TABLE country (
    id INTEGER PRIMARY KEY,
    name TEXT,
    population INTEGER,
    area INTEGER
);
''')

cursor.execute('''
CREATE TABLE city (
    id INTEGER PRIMARY KEY,
    name TEXT,
    country_id INTEGER,
    population INTEGER,
    rating INTEGER,
    FOREIGN KEY (country_id) REFERENCES country(id)
);
''')

paises = [
    (1, 'France', 66600000, 640680), (2, 'Germany', 80700000, 357000), (3, 'Brazil', 214000000, 8515000),
    (4, 'Japan', 125000000, 377000), (5, 'Canada', 38000000, 9984000), (6, 'Italy', 60000000, 301000),
    (7, 'Spain', 47000000, 505000), (8, 'Australia', 25000000, 7692000), (9, 'Mexico', 128000000, 1964000),
    (10, 'USA', 331000000, 9833000), (11, 'UK', 67000000, 243000), (12, 'Argentina', 45000000, 2780000),
    (13, 'Chile', 19000000, 756000), (14, 'Peru', 33000000, 1285000), (15, 'Colombia', 51000000, 1141000),
    (16, 'Egypt', 104000000, 1002000), (17, 'South Africa', 60000000, 1221000), (18, 'Nigeria', 211000000, 923000),
    (19, 'Kenya', 54000000, 580000), (20, 'Morocco', 37000000, 446000), (21, 'China', 1412000000, 9596000),
    (22, 'India', 1393000000, 3287000), (23, 'South Korea', 51000000, 100000), (24, 'Vietnam', 98000000, 331000),
    (25, 'Thailand', 70000000, 513000), (26, 'Sweden', 10000000, 450000), (27, 'Norway', 5000000, 385000),
    (28, 'Finland', 5000000, 338000), (29, 'Denmark', 5000000, 42000), (30, 'New Zealand', 5000000, 268000)
]


cidades = [
    (1, 'Paris', 1, 2243000, 5), (2, 'Berlin', 2, 3460000, 3), (3, 'Brasilia', 3, 3000000, 4),
    (4, 'Tokyo', 4, 14000000, 5), (5, 'Ottawa', 5, 1000000, 4), (6, 'Rome', 6, 2800000, 5),
    (7, 'Madrid', 7, 3200000, 4), (8, 'Canberra', 8, 400000, 3), (9, 'Mexico City', 9, 9000000, 3),
    (10, 'Washington DC', 10, 700000, 4), (11, 'London', 11, 8900000, 5), (12, 'Buenos Aires', 12, 3000000, 4),
    (13, 'Santiago', 13, 5600000, 3), (14, 'Lima', 14, 9700000, 3), (15, 'Bogota', 15, 7400000, 4),
    (16, 'Cairo', 16, 9500000, 2), (17, 'Pretoria', 17, 700000, 3), (18, 'Abuja', 18, 1000000, 2),
    (19, 'Nairobi', 19, 4300000, 3), (20, 'Rabat', 20, 570000, 4), (21, 'Beijing', 21, 21000000, 4),
    (22, 'New Delhi', 22, 250000, 3), (23, 'Seoul', 23, 9700000, 5), (24, 'Hanoi', 24, 4800000, 4),
    (25, 'Bangkok', 25, 8200000, 4), (26, 'Stockholm', 26, 970000, 5), (27, 'Oslo', 27, 680000, 5),
    (28, 'Helsinki', 28, 630000, 5), (29, 'Copenhagen', 29, 600000, 5), (30, 'Wellington', 30, 210000, 4)
]

cursor.executemany('INSERT INTO country VALUES (?, ?, ?, ?)', paises)
cursor.executemany('INSERT INTO city VALUES (?, ?, ?, ?, ?)', cidades)
conn.commit()


print("=== 1. Cidades com rating > 3 ===")
cursor.execute("SELECT name, rating FROM city WHERE rating > 3;")
print(cursor.fetchall()[:3])


print("\n=== 2. Cidades e Paises ===")
cursor.execute('''
SELECT city.name, country.name 
FROM city 
INNER JOIN country ON city.country_id = country.id;
''')
print(cursor.fetchall()[:3])


print("\n=== 3. Media de rating por pais >= 4 ===")
cursor.execute('''
SELECT country_id, AVG(rating) 
FROM city 
GROUP BY country_id 
HAVING AVG(rating) >= 4.0;
''')
print(cursor.fetchall()[:3])


print("\n=== 4. Cidades em ordem alfabetica ===")
cursor.execute("SELECT name FROM city ORDER BY name ASC;")
print(cursor.fetchall()[:3])
