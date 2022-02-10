import requests

# data = {
#     "username":"Julio",
#     "secret":"@admin123",
#     "info":"cargo",
#     "value":"auxiliar"
# }
# response = requests.post('http://0.0.0.0:5000/informations', data=data)

# response = requests.get('http://0.0.0.0:5000/empregados')

# response = requests.get('http://0.0.0.0:5000/empregados/Tecnico')

# response = requests.get('http://0.0.0.0:5000/empregados/salario/5000')

data = {
    "username":"Julio",
    "secret":"@admin123",
    "nome" : "Antonio",
    "cargo" : "auxiliar",
    "salario": 3500
}
response = requests.post('http://0.0.0.0:5000/register', data=data)

if response.status_code == 200:
    message = response.json()
    print(message)
else:
    print(response.status_code)
