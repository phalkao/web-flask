import sqlite3

empregados = [
    {'nome':'Catia Alencar', 'salario':5000, 'cargo':'Tecnico'},
    {'nome':'Maria Antonia', 'salario':3000, 'cargo':'Auxiliar'},
    {'nome':'Paula Oliveira', 'salario':4500, 'cargo':'Tecnico'},
    {'nome':'Mel Souza', 'salario':2500, 'cargo':'Escrituraria'},
]
 
conn = sqlite3.connect('enterprise.db')

cursor = conn.cursor()

for empregado in empregados:
    cursor.execute(""" 
        INSERT INTO empregados (nome, salario, cargo)
        VALUES(?, ?, ?)
    """, (empregado['nome'], empregado['salario'], empregado['cargo']))
 
print('Dados inseridos com sucesso!')
conn.commit()
conn.close()