import mercadopago
import requests
import json
from django.conf import settings

sdk = mercadopago.SDK(settings.MERCADO_PAGO_PRIVATE_KEY)
headers = {
    'Authorization': 'Bearer ' + settings.MERCADO_PAGO_PRIVATE_KEY
}


def __montar_payload_back_urls(request):
    back_urls = request.build_absolute_uri().replace('/pagamento/', '') + \
        '/pedido/pedido_finalizado_mercado_pago'
    return {
        "success": back_urls,
        "failure": back_urls,
        "pending": back_urls
    }


def __montar_payload_items(items):
    item_data = []
    for item in items:
        imagem = item.produto.imagem_principal.url
        
        item_data.append({
            "id": item.produto.slug,
            "title": item.produto.nome,
            "picture_url": imagem,
            # "description": item.produto.descricao,
            "category_id": item.produto.subcategoria.slug,
            "quantity": item.quantidade,
            "unit_price": float(item.modelo_produto.modelo.valor)
        })
    return item_data


def __montar_payload_payer(cliente, endereco):
    return {
        "name": cliente.user.first_name,
        "surname": cliente.user.last_name,
        "email": cliente.user.email,
        "identification": {
            "type": "CPF",
            "number": cliente.cpf
        },
        "address": {
            "street_name": endereco.endereco,
            "street_number": endereco.numero,
            "zip_code": endereco.cep,
        },
        "shipments": {
            "receiver_address": {
                "street_name": endereco.endereco,
                "street_number": endereco.numero,
                "zip_code": endereco.cep
            }
        }
    }


def montar_payload_preference(request, pedido_uuid, items, cliente, endereco, valor_frete):

    item_data = __montar_payload_items(items)
    payer = __montar_payload_payer(cliente, endereco)
    back_urls = __montar_payload_back_urls(request)

    return {
        "back_urls": back_urls,
        "payer": payer,
        "auto_return": "all",
        "items": item_data,
        "statement_descriptor": "LIKEESTAMPA",
        "external_reference": str(pedido_uuid),
        "installments": 1,
        "excluded_payment_types": [
            {
                "id": "ticket"
            }
        ],
        "shipments": {
            "cost": float(valor_frete),
            "mode": "not_specified",
        }
    }


def create_preference(preference_data):
    response = sdk.preference().create(preference_data)
    return response["response"]


def get_payment(payment_id):
    url = 'https://api.mercadopago.com/v1/payments/' + str(payment_id)
    r = requests.get(url, headers=headers)
    return json.loads(r.text)


def get_merchant_order(merchant_order_id):
    url = 'https://api.mercadopago.com/merchant_orders/' + str(merchant_order_id)
    r = requests.get(url, headers=headers)
    return json.loads(r.text)


def get_preference(preference_id):
    url = 'https://api.mercadopago.com/checkout/preferences/' + str(preference_id)
    r = requests.get(url, headers=headers)
    return json.loads(r.text)

def get_pagamento_by_external_reference(external_reference):
    url = 'https://api.mercadopago.com/v1/payments/search?sort=date_created&criteria=desc&external_reference=' + str(external_reference)
    r = requests.get(url, headers=headers)
    return json.loads(r.text)


def confirma_pagamento(payment_id):
    """ Confirma se realmente foi pago. Ex em caso que o usuario pode mudar a session."""
    try:
        pagamento = get_payment(payment_id)
        if pagamento['status'] == 'approved':
            return True
    except:
        return False

    return False
