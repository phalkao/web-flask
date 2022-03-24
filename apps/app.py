from flask import Flask, render_template, request, url_for, redirect, Response, jsonify, g
from flask_restful import Resource, Api
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs

from datetime import datetime
from random import randrange
import sqlite3
import json
from os import uname

from apps.apis import employees

DB_URL = 'enterprise.db'

users = [
    {'id':1, 'username':'Julio', 'secret':'@admin123'}
]

# Flask app instance initiated
app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

# Flask restful wraps Flask app around it.#  Restful way of creating APIs through Flask Restful
api = Api(app)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='WebFlask Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/doc/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/doc-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)


class WebFlaskResponseSchema(Schema):
    message = fields.Str(default='Success')


class WebFlaskRequestSchema(Schema):
    api_type = fields.String(required=True, description="API type of web-flask API")


#  Restful way of creating APIs through Flask Restful
class WebFlaskAPI(MethodResource, Resource):
    @doc(description='My First GET WebFlask API.', tags=['WebFlask'])
    @marshal_with(WebFlaskResponseSchema)  # marshalling
    def get(self):
        '''
        Get method represents a GET API method
        '''
        return {'message': 'My First WebFlask API'}

    @doc(description='My First GET WebFlask API.', tags=['WebFlask'])
    @use_kwargs(WebFlaskRequestSchema, location=('json'))
    @marshal_with(WebFlaskResponseSchema)  # marshalling
    def post(self, **kwargs):
        '''
        Get method represents a GET API method
        '''
        return {'message': 'My First WebFlask API'}


api.add_resource(WebFlaskAPI, '/awesome')
docs.register(WebFlaskAPI)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

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

def query_employee_to_dict(ini, query):
    cursor = g.conn.cursor()
    cursor.execute(query)

    employees = [
        {'id' : row[0], 'nome' : row[1], 'nascimento' : row[2], 'sexo' : row[3], 'cargo' : row[4], 'salario' : row[5], 'cadastro' : row[6]}
        for row in cursor.fetchall()
    ]

    return {
        '_ini': ini,
        '_machine' : uname().nodename,    
        'employees' : employees
    }

def check_user(username, secret):
    for user in users:
        if (user["username"] == username) and (user["secret"] == secret):
            return True
    return False

@app.route('/')
def home():
    return render_template('/site/home.html', machine=uname().nodename)

@app.route('/dashboard')
def dashboard():
    return render_template('/dashboard/home.html', machine=uname().nodename)

@app.route('/empregados')
def get_empregados():
    ini = randrange(32743)

    return query_employee_to_dict(ini, employees.empregados(ini))

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


def run(debug=True, host="0.0.0.0"):
    app.run(debug=debug, host=host)
