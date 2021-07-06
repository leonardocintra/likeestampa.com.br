import requests
import json

URL_DIMONA = "https://camisadimona.com.br/api/v2"

HEADERS = {
    'api-key': 'f9bb66ac5feaebd7b97206198866a898',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


def get_frete(cep, quantidade):
    payload = json.dumps({
        "zipcode": cep,
        "quantity": quantidade
    })

    response = requests.request(
        "POST", URL_DIMONA + "/shipping", headers=HEADERS, data=payload)

    return json.loads(response.text)


def create_order():
    payload = json.dumps({
        "shipping_speed": "sedex",
        "order_id": "1625584335",
        "customer_name": "Fulano da Silva",
        "items": [
            {
                "name": "Camisa P Amarela",
                "sku": "12345",
                "qty": 2
            },
            {
                "name": "Camisa M Verde",
                "sku": "12346",
                "qty": 1
            },
            {
                "name": "Camisa G Vermelha",
                "sku": "12347",
                "qty": 1
            }
        ],
        "address": {
            "street": "Rua Buenos Aires",
            "number": "334",
            "complement": "Loja",
            "city": "Rio de Janeiro",
            "state": "RJ",
            "zipcode": "20061001",
            "neighborhood": "Centro"
        }
    })

    response = requests.request(
        "POST", URL_DIMONA + "/order", headers=HEADERS, data=payload)
    print(response.text)
