from django.conf import settings
import requests
import json

headers = {
    'Authorization': settings.MELHOR_ENVIO_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'User-Agent': 'LikeEstampa (likeestampa@gmail.com)',
}

BASE_URL = settings.MELHOR_ENVIO_BASE_URL


def get_cotacao_frete(items, cep_origem, cep_destino):
    url = BASE_URL + '/api/v2/me/shipment/calculate'

    item_data = []
    for item in items:        
        item_data.append({
            "id": item.produto.slug,
            "width": 15,
            "height": 4,
            "length": 15,
            "weight": 0.180,
            "insurance_value": 0, #float(item.produto.preco_base),
            "quantity": item.quantidade
        })

    payload = json.dumps({
        "from": {
            "postal_code": cep_origem
        },
        "to": {
            "postal_code": cep_destino
        },
        "products": item_data
    })

    r = requests.post(url, data=payload, headers=headers)
    return json.loads(r.text)
