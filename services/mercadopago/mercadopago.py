import mercadopago
import requests
import json
from django.conf import settings

sdk = mercadopago.SDK(settings.MERCADO_PAGO_PRIVATE_KEY)
headers = {
    'Authorization': 'Bearer ' + settings.MERCADO_PAGO_PRIVATE_KEY
}


def create_preference(preference_data):
    response = sdk.preference().create(preference_data)
    return response["response"]


def get_payment(payment_id):
    url = 'https://api.mercadopago.com/v1/payments/' + payment_id
    r = requests.get(url, headers=headers)

    return json.loads(r.text)


def get_preference(preference_id):
    url = 'https://api.mercadopago.com/checkout/preferences/' + preference_id
    r = requests.get(url, headers=headers)

    return json.loads(r.text)
