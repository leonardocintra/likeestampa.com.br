from django.conf import settings
import requests
import json

BASE_URL = settings.PEOPLE_SOFT_API

HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


def cadastrar_cliente(cliente):
    cliente_existe = buscar_cliente_by_cpf(cliente['cpf'])

    if cliente_existe:
        return cliente_existe['records'][0]['id']
        # TODO: verificar tambem se o endereco ainda eh o mesmo

    data = {
        'nome': cliente['nome'] + ' ' + cliente['sobrenome'],
        'cpf': cliente['cpf'],
        'sexo': cliente['sexo'],
        'email': cliente['email'],
        'enderecos': [
            {
                'cep': cliente['cep'],
                'endereco': cliente['endereco'],
                'numero': cliente['numero'],
                'bairro': cliente['bairro'],
                'cidade': cliente['cidade'],
                'uf': cliente['uf'],
                'referencia': cliente['referencia'],
                'complemento': cliente['complemento'],
            }
        ],
        'telefones': [
            {
                'area': cliente['area'],
                'numero': cliente['telefone_numero'],
                'tipo': cliente['tipo']
            }
        ]
    }

    response = requests.post(BASE_URL + '/pessoa',
                             data=json.dumps(data), headers=HEADERS)

    cliente_json = json.loads(response.text)

    if response.status_code == 201:
        return cliente_json['records'][0]['id']
    elif response.status_code == 409:
        # TODO: colocar tratamento para caso email ja existe
        cliente_json = buscar_cliente_by_id(cliente['id'])
        return cliente_json['records'][0]['id']
    else:
        print(response.text)
        # TODO: Enviar erro no telegram


def buscar_cliente_by_cpf(cpf):
    response = requests.get(BASE_URL + '/pessoa/cpf/' + cpf, headers=HEADERS)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print(response.text)


def buscar_cliente_by_id(id):
    response = requests.get(BASE_URL + '/pessoa/' + str(id), headers=HEADERS)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print(response.text)
