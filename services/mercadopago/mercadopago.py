import mercadopago
import json
from django.conf import settings

sdk = mercadopago.SDK(settings.MERCADO_PAGO_PRIVATE_KEY)


def create_preference(preference_data):
    response = sdk.preference().create(preference_data)
    return response["response"]
