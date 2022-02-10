from flask import Flask, render_template, request, url_for, redirect, Response, jsonify, g
from datetime import datetime
from random import randrange
import sqlite3
import json
from os import uname

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

DB_URL = 'enterprise.db'

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
        {'id' : row[0], 'nome' : row[1], 'nascimento' : row[2], 'sexo' : row[3], 'cargo' : row[4], 'salario' : row[5], 'cadastro' : row[6]}
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
    return render_template('home.html', machine=uname().nodename)

@app.route('/empregados')
def get_empregados():
    ini = randrange(32743)

    query = f"""
        SELECT id, nome, nascimento, sexo, cargo, salario, cadastro 
        FROM empregados LIMIT {ini}, 100;
    """
    employees = query_employee_to_dict(g.conn, query)

    return {
        '_ini': ini,
        '_machine' : uname().nodename,    
        'employees' : employees
    }

@app.route('/empregados/<cargo>')
def get_empregados_cargo(cargo):
    ini = randrange(32743)

    query = """
        SELECT id, nome, nascimento, sexo, cargo, salario, cadastro 
        FROM empregados
        WHERE "cargo" LIKE "%{}%" LIMIT {ini}, 100;
    """.format(cargo)
    
    employees = query_employee_to_dict(g.conn, query)

    return {
        '_ini': ini,
        '_machine' : uname().nodename,    
        'employees' : employees
    }

@app.route('/empregados/<info>/<value>')
def get_empregados_info_value(info, value):
    ini = randrange(32743)
    
    if value.isnumeric():
        value = float(value)

    query = """
        SELECT id, nome, nascimento, sexo, cargo, salario, cadastro 
        FROM empregados
        WHERE "{}" LIKE "%{}%" LIMIT {}, 100;
    """.format(info, value, ini)
    
    employees = query_employee_to_dict(g.conn, query)

    return {
        '_ini': ini,
        '_machine' : uname().nodename,    
        'employees' : employees
    }

@app.route('/informations', methods=['POST'])
def get_empregados_post():
    ini = randrange(32743)

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
        SELECT id, nome, nascimento, sexo, cargo, salario, cadastro 
        FROM empregados
        WHERE "{}" LIKE "%{}% LIMIT {ini}, 100";
    """.format(info, value)
    
    employees = query_employee_to_dict(g.conn, query)

    return {
        '_ini': ini,
        '_machine' : uname().nodename,    
        'employees' : employees
    }

@app.route('/register', methods=['POST'])
def add_empregados_post():
    username = request.form['username']
    secret = request.form['secret']

    if not check_user(username, secret):
        # 401 HTTP Unauthorized
        return Response("Unauthorized", status=401)

    nome = request.form['nome']
    nascimento = request.form['nascimento']
    sexo = request.form['sexo']
    cargo = request.form['cargo']
    salario = request.form['salario']
    cadastro = datetime.today().strftime('%Y-%m-%d')

    query = """
        INSERT INTO empregados (nome, nascimento, sexo, cargo, salario, cadastro) 
        VALUES ("{}", "{}", "{}", "{}", "{}", "{}");
    """.format(nome, nascimento, sexo, cargo, salario, cadastro)
    
    cursor = g.conn.cursor()
    cursor.execute(query)
    g.conn.commit()

    return {
        '_machine' : uname().nodename,    
        'employees' : 'Registered employee...'
    }


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")