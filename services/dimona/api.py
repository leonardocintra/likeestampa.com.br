import requests
import json

URL_DIMONA = "https://camisadimona.com.br/api/v2"

HEADERS = {
    'api-key': 'f9bb66ac5feaebd7b97206198866a898',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


def get_timeline(pedido_dimona):
    response = requests.get(URL_DIMONA + '/order/' +
                            pedido_dimona + '/timeline', headers=HEADERS)
    print(response.text)
    return json.loads(response.text)


def get_tracking(pedido_dimona):
    response = requests.get(URL_DIMONA + '/order/' +
                            pedido_dimona + '/tracking', headers=HEADERS)
    print(response.text)
    return json.loads(response.text)


def get_frete(cep, quantidade):
    payload = json.dumps({
        "zipcode": cep,
        "quantity": quantidade
    })

    response = requests.post(URL_DIMONA + "/shipping",
                             headers=HEADERS, data=payload)
    return json.loads(response.text)


def create_order(order_id, cliente, items, delivery_method_id):

    cliente = cliente['records'][0]
    endereco = cliente['enderecos'][0]
    tel_numero = '999999999'

    if cliente['telefones']:
        telefone = cliente['telefones'][0]
        tel_numero = telefone['area'] + telefone['numero']

    items_request = _monta_payload_item(items)

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
    return json.loads(response.text)


def _monta_payload_item(items):
    skus = requests.get('https://run.mocky.io/v3/fe9e4b43-f3e7-480a-ac23-625db3e24ba7')

    item_request = []
    for item in items:
        imagem_design = ''
        if item.produto.imagem_design:
            imagem_design = item.produto.imagem_design.url

        cor = item.cor.tipo_variacao.descricao
        tamanho = item.tamanho.tipo_variacao.descricao
        modelo = ''
        if item.modelo.nome == 'TRADICIONAL':
            modelo = 'T-Shirt'
        
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
    for sku in json.loads(skus.content):
        if sku['Estilo'] == modelo and sku['Cor'] == cor and sku['Tamanho'] == tamanho:
            return sku['codigoSku']
    #TODO: informar que esta errado (aviso telegram por exemplo)
    return "10110110110"