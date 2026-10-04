/* ============================================================
   RESOLUÇÃO DA LISTA PRÁTICA - BANCO DE DADOS (POSTGRESQL)
   ============================================================ */

-- Reset do esquema para recriação limpa das tabelas
DROP TABLE IF EXISTS Consulta, Paciente, Medico, Especialidade, venda, produto, vendedor CASCADE;

-- ------------------------------------------------------------
-- Bloco 01: Módulo de Vendas e Consultas Agregadas (Item 10)
-- ------------------------------------------------------------

CREATE TABLE vendedor (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    data_nascimento DATE,
    salario NUMERIC(10,2) DEFAULT 0.00
);

CREATE TABLE produto (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco NUMERIC(10,2) NOT NULL
);

CREATE TABLE venda (
    id SERIAL PRIMARY KEY,
    id_vendedor INT,
    id_produto INT,
    valor NUMERIC(10,2) NOT NULL,
    data_venda DATE,
    CONSTRAINT fk_vendedor FOREIGN KEY (id_vendedor) REFERENCES vendedor(id),
    CONSTRAINT fk_produto FOREIGN KEY (id_produto) REFERENCES produto(id)
);

-- Carga inicial de registros de vendas
INSERT INTO vendedor (nome, data_nascimento, salario) VALUES
    ('Ana Silva', '1990-05-15', 1500.00),
    ('Carlos Nogueira', '1985-08-20', 1800.00),
    ('Renata Costa', '1995-03-10', 2000.00);

INSERT INTO produto (nome, preco) VALUES
    ('martelo', 25.50),
    ('chave de fenda', 15.00),
    ('alicate', 30.00);

INSERT INTO venda (id_vendedor, id_produto, valor, data_venda) VALUES
    (1, 1, 500.00, '2026-01-10'),
    (1, 2, 600.00, '2026-02-15'),
    (2, 1, 25.50, '2026-03-01'),
    (3, 3, 300.00, '2026-03-05');

-- Queries de validação (Questão 10)
SELECT * FROM vendedor;

SELECT id, nome, data_nascimento, salario 
FROM vendedor 
ORDER BY nome ASC;

SELECT nome FROM vendedor WHERE nome ILIKE '%na%';

SELECT SUM(valor) AS montante_total FROM venda;

SELECT id_vendedor, SUM(valor) AS total_por_vendedor 
FROM venda 
GROUP BY id_vendedor;

SELECT DISTINCT vend.nome, vend.data_nascimento 
FROM vendedor vend 
INNER JOIN venda v ON vend.id = v.id_vendedor;

SELECT DISTINCT vend.nome 
FROM vendedor vend 
INNER JOIN venda v ON vend.id = v.id_vendedor 
INNER JOIN produto prod ON prod.id = v.id_produto 
WHERE prod.nome ILIKE 'martelo';

SELECT COUNT(id) AS qtd_vendedores FROM vendedor;

-- Atualização salarial baseada no volume de vendas (> 1000)
UPDATE vendedor 
SET salario = salario + 100.00 
WHERE id IN (
    SELECT id_vendedor 
    FROM venda 
    GROUP BY id_vendedor 
    HAVING SUM(valor) > 1000
);


-- ------------------------------------------------------------
-- Bloco 02: Gestão Médica e Subqueries com IN (Itens 14 e 15)
-- ------------------------------------------------------------

CREATE TABLE Medico (
    id INT PRIMARY KEY,
    nome VARCHAR(50),
    altura NUMERIC(3,2)
);

INSERT INTO Medico (id, nome, altura) VALUES
    (1, 'M1', 1.70),
    (2, 'M2', 1.80),
    (3, 'M3', 1.90),
    (4, 'M4', 1.68);

-- 14. Identificação do médico com maior estatura
SELECT nome 
FROM Medico 
WHERE altura IN (SELECT MAX(altura) FROM Medico);

-- 15. Cadastro de M5 e busca do médico com menor estatura
INSERT INTO Medico (id, nome, altura) VALUES (5, 'M5', 1.68);

SELECT nome 
FROM Medico 
WHERE altura IN (SELECT MIN(altura) FROM Medico);


-- ------------------------------------------------------------
-- Bloco 03: Histórico de Consultas e Pacientes (Itens 16 e 17)
-- ------------------------------------------------------------

CREATE TABLE Paciente (
    id INT PRIMARY KEY,
    nome VARCHAR(50)
);

INSERT INTO Paciente (id, nome) VALUES (1, 'P1'), (2, 'P2'), (3, 'P3');

CREATE TABLE Consulta (
    id INT PRIMARY KEY,
    idPaciente INT REFERENCES Paciente(id),
    idMedico INT REFERENCES Medico(id),
    data DATE
);

INSERT INTO Consulta (id, idPaciente, idMedico, data) VALUES
    (1, 1, 1, '2016-10-10'),
    (2, 2, 1, '2016-12-05'),
    (3, 3, 2, '2017-02-03'),
    (4, 1, 3, '2016-12-15');

-- 16. Corpo médico com agendamentos em dezembro de 2016
SELECT nome 
FROM Medico 
WHERE id IN (
    SELECT idMedico 
    FROM Consulta 
    WHERE data >= '2016-12-01' AND data <= '2016-12-31'
);

-- 17. Atualização estrutural e seleção de pacientes (> 21 anos)
ALTER TABLE Paciente ADD COLUMN Idade INT;

UPDATE Paciente SET Idade = 10 WHERE id = 1;
UPDATE Paciente SET Idade = 22 WHERE id = 2;
UPDATE Paciente SET Idade = 38 WHERE id = 3;

SELECT nome 
FROM Paciente 
WHERE Idade > 21 
  AND id IN (SELECT idPaciente FROM Consulta);


-- ------------------------------------------------------------
-- Bloco 04: Operadores Lógicos Avancados (ANY, ALL e EXISTS)
-- ------------------------------------------------------------

-- 18. Filtro utilizando o operador ANY
SELECT nome 
FROM Paciente 
WHERE Idade > ANY (SELECT Idade FROM Paciente);

-- 19. Tabela de especialidades e filtragem com operador ALL
CREATE TABLE Especialidade (
    Id INT PRIMARY KEY,
    nome VARCHAR(50)
);

INSERT INTO Especialidade (Id, nome) VALUES
    (1, 'Cardiologia'), 
    (2, 'Ortopedia'), 
    (3, 'Pediatria');

ALTER TABLE Medico ADD COLUMN salario NUMERIC(10,2);
ALTER TABLE Medico ADD COLUMN idEspecialidade INT REFERENCES Especialidade(Id);

UPDATE Medico SET salario = 1000, idEspecialidade = 3 WHERE id = 1;
UPDATE Medico SET salario = 5000, idEspecialidade = 2 WHERE id = 2;
UPDATE Medico SET salario = 10000, idEspecialidade = 1 WHERE id = 3;
UPDATE Medico SET salario = 12000, idEspecialidade = 3 WHERE id = 4;
UPDATE Medico SET salario = 15000, idEspecialidade = 1 WHERE id = 5;

SELECT nome 
FROM Medico 
WHERE salario > ALL (
    SELECT salario 
    FROM Medico 
    WHERE idEspecialidade IN (
        SELECT Id FROM Especialidade WHERE nome ILIKE 'Pediatria'
    )
);

-- 20. Inclusão de P4 e validação de consultas com EXISTS e IN
INSERT INTO Paciente (id, nome, Idade) VALUES (4, 'P4', 44);

-- 20 a) Verificação via EXISTS
SELECT nome 
FROM Paciente pac
WHERE EXISTS (
    SELECT 1 
    FROM Consulta con 
    WHERE con.idPaciente = pac.id
);

-- 20 b) Verificação via IN
SELECT nome 
FROM Paciente 
WHERE id IN (SELECT idPaciente FROM Consulta);