from flask import Flask, render_template, request, url_for, redirect, Response, jsonify, g
import sqlite3

app = Flask(__name__)

DB_URL = 'enterprise.db'

# employees = [
#     {'id':1, 'name':'Catia Alencar', 'salary':5000, 'age': 27, 'position':'Tecnico'},
#     {'id':2, 'name':'Maria Antonia', 'salary':3000, 'age': 25, 'position':'Auxiliar'},
#     {'id':3, 'name':'Paula Oliveira', 'salary':4500, 'age': 30, 'position':'Tecnico'},
#     {'id':4, 'name':'Mel Souza', 'salary':2500, 'age': 18, 'position':'Escrituraria'},
# ]

users = [
    {'id':1, 'username':'Julio', 'secret':'@admin123'}
]

@app.before_request
def before_request():
    print('Conectando ao banco de dados!')
    conn = sqlite3.connect(DB_URL)
    g.conn = conn

@app.teardown_request
def after_request(exception):
    if g.conn is not None:
        g.conn.close()
        print('Desconectando do banco de dados!')

def query_employee_to_dict(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)

    employees = [
        {'id' : row[0], 'nome' : row[1], 'salario' : row[2], 'cargo' : row[3]}
        for row in cursor.fetchall()
    ]

    return employees



def check_user(username, secret):
    for user in users:
        if (user["username"] == username) and (user["secret"] == secret):
            return True
    return False



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/empregados')
def get_empregados():
    query = """
        SELECT id, nome, salario, cargo 
        FROM empregados;
    """
    
    employees = query_employee_to_dict(g.conn, query)

    return {'employees' : employees}

@app.route('/empregados/<cargo>')
def get_empregados_cargo(cargo):
    query = """
        SELECT id, nome, salario, cargo 
        FROM empregados
        WHERE "cargo" LIKE "%{}%";
    """.format(cargo)
    
    employees = query_employee_to_dict(g.conn, query)

    return {'empregados' : employees}

@app.route('/empregados/<info>/<value>')
def get_empregados_info_value(info, value):
    
    if value.isnumeric():
        value = float(value)

    query = """
        SELECT id, nome, salario, cargo 
        FROM empregados
        WHERE "{}" LIKE "%{}%";
    """.format(info, value)
    
    employees = query_employee_to_dict(g.conn, query)

    return {'empregados' : employees}

@app.route('/informations', methods=['POST'])
def get_empregados_post():

    username = request.form['username']
    secret = request.form['secret']

    if not check_user(username, secret):
        # 401 HTTP Unauthorized
        return Response("Unauthorized", status=401)

    info = request.form['info']
    value = request.form['value']

    if value.isnumeric():
        value = float(value)

    query = """
        SELECT id, nome, salario, cargo 
        FROM empregados
        WHERE "{}" LIKE "%{}%";
    """.format(info, value)
    
    employees = query_employee_to_dict(g.conn, query)

    return {'empregados' : employees}

@app.route('/register', methods=['POST'])
def add_empregados_post():

    username = request.form['username']
    secret = request.form['secret']

    if not check_user(username, secret):
        # 401 HTTP Unauthorized
        return Response("Unauthorized", status=401)

    nome = request.form['nome']
    cargo = request.form['cargo']
    salario = request.form['salario']

    query = """
        INSERT INTO empregados (nome, cargo, salario) 
        VALUES ("{}", "{}", "{}");
    """.format(nome, cargo, salario)
    
    cursor = g.conn.cursor()
    cursor.execute(query)
    g.conn.commit()

    return {'empregados' : 'Registered employee...'}


if __name__ == '__main__':
    app.run(debug=True)