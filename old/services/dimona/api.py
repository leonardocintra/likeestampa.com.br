import requests
import json
from django.conf import settings
from sentry_sdk import capture_exception

from apps.catalogo.models import SkuDimona
from apps.pedido.models import Pedido
from services.telegram.api import enviar_mensagem


URL_DIMONA = "https://camisadimona.com.br/api/v2"

HEADERS = {
    'api-key': settings.DIMONA_KEY,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


def get_tracking_url(pedido_dimona):
    try:
        response = requests.get(
            URL_DIMONA + '/order/' + pedido_dimona, headers=HEADERS)
        return json.loads(response.text)
    except Exception as e:
        capture_exception(e)
        return {
            "tracking_url": "",
        }


def get_timeline(pedido_dimona):
    try:
        response = requests.get(URL_DIMONA + '/order/' +
                                pedido_dimona + '/timeline', headers=HEADERS)
        return json.loads(response.text)
    except Exception as e:
        capture_exception(e)
        return None


def get_tracking(pedido_dimona):
    response = requests.get(URL_DIMONA + '/order/' +
                            pedido_dimona + '/tracking', headers=HEADERS)
    return json.loads(response.text)


def get_frete(cep, quantidade):
    payload = json.dumps({
        "zipcode": cep,
        "quantity": quantidade
    })

    response = requests.post(URL_DIMONA + "/shipping",
                             headers=HEADERS, data=payload)
    return json.loads(response.text)


def create_payload_order(order_id, cliente, endereco, items, delivery_method_id):
    tel_numero = '99999999999'

    if cliente.telefone:
        tel_numero = cliente.telefone

    items_request = __monta_payload_item(items, order_id)

    payload = json.dumps(
        {
            "delivery_method_id": delivery_method_id,
            "order_id": order_id,
            "customer_name": cliente.user.first_name + ' ' + cliente.user.last_name,
            "customer_document": cliente.cpf,
            "customer_email": cliente.user.email,
            "webhook_url": "https://option_webhook_url.com",
            "items": items_request,
            "address": {
                "street": endereco.endereco,
                "number": endereco.numero,
                "complement": endereco.complemento,
                "city": endereco.cidade,
                "state": endereco.uf,
                "zipcode": endereco.cep,
                "neighborhood": endereco.bairro,
                "phone": tel_numero,
                "country": "BR"
            }
        }
    )
    Pedido.objects.filter(pk=order_id).update(request_seller=payload)


def create_order(payload):
    return requests.post(URL_DIMONA + "/order",
                         headers=HEADERS, data=payload)


def __monta_payload_item(items, order_id):
    skus = SkuDimona.objects.all()

    item_request = []
    for item in items:
        imagem_design = ''
        if item.produto.imagem_design:
            imagem_design = item.produto.imagem_design.url

        cor = item.cor
        tamanho = item.tamanho
        modelo_produto = item.modelo_produto.modelo.descricao

        item_request.append({
            "name": item.produto.nome,
            "sku": item.produto.slug,
            "qty": item.quantidade,
            "dimona_sku_id": __get_sku_dimona(skus, modelo_produto, tamanho, cor, order_id),
            "designs": [
                imagem_design
            ],
            "mocks": [
                item.produto.imagem_principal.url
            ]
        })
    return item_request


def __get_sku_dimona(skus, modelo_produto, tamanho, cor, order_id):
    skus = skus.filter(cor=cor.nome)
    skus = skus.filter(tamanho=tamanho.nome)
    for sku in skus:
        if sku.estilo.descricao == modelo_produto and sku.cor == cor.nome and sku.tamanho == tamanho.nome and sku.estilo.descricao == modelo_produto:
            return sku.sku
    enviar_mensagem('SKU DIMONA não encontrado.\n -Modelo: {0} \n -Tamanho: {1} \n -Cor: {2}'.format(
        modelo_produto, tamanho, cor), 'SKU não encontrado', str(order_id))
    return 999999999
