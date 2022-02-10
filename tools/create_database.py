import sqlite3

conn = sqlite3.connect('enterprise.db')

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE empregados (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT(200) NOT NULL ,
        nascimento TEXT(10),
        sexo TEXT(1),
        cargo TEXT(100),
        salario REAL,
        cadastro TEXT(10)
    );
""")

print("Tabela criada com sucesso!")

conn.close()