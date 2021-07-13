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


def create_order(order_id, cliente, items, delivery_method_id):
    
    cliente = cliente['records'][0]
    endereco = cliente['enderecos'][0]
    tel_numero = '999999999'

    if cliente['telefones']:
        telefone = cliente['telefones'][0]
        tel_numero = telefone['area'] + telefone['numero']

    items_request = monta_payload_item(items)

    payload = json.dumps(
        {
            "delivery_method_id": delivery_method_id,
            "order_id": order_id,
            "customer_name": cliente['nome'],
            "customer_document": cliente['cpf'],
            "customer_email": cliente['email'],
            "webhook_url": "https://option_webhook_url.com",
            "items": items_request,
            "address": {
                "street": endereco['endereco'],
                "number": endereco['numero'],
                "complement": endereco['complemento'],
                "city": endereco['cidade'],
                "state": endereco['uf'],
                "zipcode": endereco['cep'],
                "neighborhood": endereco['bairro'],
                "phone": tel_numero,
                "country": "BR"
            }
        }
    )

    response = requests.post(URL_DIMONA + "/order",
                             headers=HEADERS, data=payload)
    print(response.text)


def monta_payload_item(items):
    item_request = []
    for item in items:
        item_request.append({
            "name": item.produto.nome,
            "sku": item.produto.slug,
            "qty": item.quantidade,
            "dimona_sku_id": "10110110110",
            "designs": [
                "url_front"
            ],
            "mocks": [
                "mock_front"
            ]
        })
    return item_request
