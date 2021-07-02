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


def get_cotacao_frete():
    url = BASE_URL + '/api/v2/me/shipment/calculate'

    payload = json.dumps({
        "from": {
            "postal_code": "13306705"
        },
        "to": {
            "postal_code": "14408114"
        },
        "products": [
            {
                "id": "x",
                "width": 11,
                "height": 17,
                "length": 11,
                "weight": 0.3,
                "insurance_value": 10.1,
                "quantity": 1
            },
            {
                "id": "y",
                "width": 16,
                "height": 25,
                "length": 11,
                "weight": 0.3,
                "insurance_value": 55.05,
                "quantity": 2
            },
            {
                "id": "z",
                "width": 22,
                "height": 30,
                "length": 11,
                "weight": 1,
                "insurance_value": 30,
                "quantity": 1
            }
        ]
    })

    r = requests.post(url, data=payload, headers=headers)
    return json.loads(r.text)
