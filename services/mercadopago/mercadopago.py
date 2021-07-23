import mercadopago
import requests
import json
from django.conf import settings

sdk = mercadopago.SDK(settings.MERCADO_PAGO_PRIVATE_KEY)
headers = {
    'Authorization': 'Bearer ' + settings.MERCADO_PAGO_PRIVATE_KEY
}


def montar_payload_back_urls(request):
    back_urls = request.build_absolute_uri().replace('/pagamento/', '') + \
        '/pedido/pedido_finalizado_mercado_pago'
    return {
        "success": back_urls,
        "failure": back_urls,
        "pending": back_urls
    }


def montar_payload_items(items):
    item_data = []
    for item in items:
        imagem = item.produto.imagem_principal.url
        if item.cor.imagem:
            imagem = item.cor.imagem.url

        item_data.append({
            "id": item.produto.slug,
            "title": item.produto.nome,
            "picture_url": imagem,
            # "description": item.produto.descricao,
            "category_id": item.produto.subcategoria.slug,
            "quantity": item.quantidade,
            "unit_price": float(item.produto.preco_base)
        })
    return item_data


def montar_payload_payer(cliente, endereco):
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


def montar_payload_preference(request, pedido_id, items, cliente, endereco, valor_frete):

    item_data = montar_payload_items(items)
    payer = montar_payload_payer(cliente, endereco)
    back_urls = montar_payload_back_urls(request)

    return {
        "back_urls": back_urls,
        "payer": payer,
        "auto_return": "approved",
        "items": item_data,
        "statement_descriptor": "LIKE_ESTAMPA",
        "external_reference": "LIKEESTAMPA-" + str(pedido_id),
        "installments": 10,
        "shipments": {
            "cost": float(valor_frete),
            "mode": "not_specified",
        }
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
