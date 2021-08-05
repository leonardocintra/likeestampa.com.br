import requests
import json
from random import randint
from django.conf import settings
from catalogo.models import SkuDimona
from pedido.models import Pedido

URL_DIMONA = "https://camisadimona.com.br/api/v2"

HEADERS = {
    'api-key': 'f9bb66ac5feaebd7b97206198866a898',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


def get_tracking_url(pedido_dimona):
    try:
        response = requests.get(
            URL_DIMONA + '/order/' + pedido_dimona, headers=HEADERS)
        return json.loads(response.text)
    except:
        return {
            "tracking_url": "",
        }


def get_timeline(pedido_dimona):
    try:
        response = requests.get(URL_DIMONA + '/order/' +
                                pedido_dimona + '/timeline', headers=HEADERS)
        return json.loads(response.text)
    except print(0):
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


def create_order(order_id, cliente, endereco, items, delivery_method_id):
    tel_numero = '999999999'

    if cliente.telefone:
        tel_numero = cliente.telefone

    items_request = _monta_payload_item(items)

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
    if settings.DEBUG:
        return _get_fake_dimona_order_id()
    response = requests.post(URL_DIMONA + "/order",
                             headers=HEADERS, data=payload)
    return json.loads(response.text)


def _monta_payload_item(items):
    skus = SkuDimona.objects.all()

    item_request = []
    for item in items:
        imagem_design = ''
        if item.produto.imagem_design:
            imagem_design = item.produto.imagem_design.url

        cor = item.cor.tipo_variacao.descricao
        tamanho = item.tamanho.tipo_variacao.descricao
        modelo = item.modelo.modelo.descricao

        item_request.append({
            "name": item.produto.nome,
            "sku": item.produto.slug,
            "qty": item.quantidade,
            "dimona_sku_id": _get_sku_dimona(skus, modelo, tamanho, cor),
            "designs": [
                imagem_design
            ],
            "mocks": [
                item.produto.imagem_principal.url
            ]
        })
    return item_request


def _get_sku_dimona(skus, modelo, tamanho, cor):
    skus = skus.filter(cor=cor)
    skus = skus.filter(tamanho=tamanho)
    for sku in skus:
        if sku.estilo.descricao == modelo and sku.cor == cor and sku.tamanho == tamanho and sku.nome == 'Dimona Quality':
            return sku.sku
    # TODO: informar que esta errado (aviso telegram por exemplo)
    return 10110110110


def _get_fake_dimona_order_id():
    # Quando nao estiver no ambiente de producao, geraremos um pedido fake
    range1 = str(randint(100, 999))
    range2 = str(randint(100, 999))
    range3 = str(randint(100, 999))
    return {"order": "{0}-{1}-{2}".format(range1, range2, range3)}
