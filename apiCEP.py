import requests

def responseJSON(method, url, headers=[], payload=[], files=[]):
    response = requests.request(method,  url, headers=headers, data=payload, files=files)

    print(response.text)

if __name__ == "__main__":
    # https://docs.awesomeapi.com.br/api-cep
    endpoint = "https://cep.awesomeapi.com.br/json/05424020"

    responseJSON('GET', endpoint)


"""
    {
        "cep":"05424020",
        "address_type":"Rua",
        "address_name":"Professor Carlos Reis",
        "address":"Rua Professor Carlos Reis",
        "state":"SP",
        "district":"Pinheiros",
        "lat":"-23.57021",
        "lng":"-46.69685",
        "city":"São Paulo",
        "city_ibge":"3550308",
        "ddd":"11"
    }
"""

