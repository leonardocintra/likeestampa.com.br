import requests
import json

URL_DIMONA = "https://camisadimona.com.br/api/v2/shipping"

HEADERS = {
    'api-key': 'f9bb66ac5feaebd7b97206198866a898',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

def get_frete(frete):
    payload = json.dumps({
        "zipcode": frete,
        "quantity": "1"
    })

    response = requests.request("POST", URL_DIMONA, headers=HEADERS, data=payload)

    fretes = json.loads(response.text)
    menor_preco = 0

    for f in fretes:
        if menor_preco == 0:
            menor_preco = f['value']
        elif menor_preco > f['value']:
            menor_preco = f['value']

    return menor_preco
