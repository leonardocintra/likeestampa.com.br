from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
# from django.utils.functional import cached_property
from checkout.models import Carrinho, ItemCarrinho
from services.mercadopago.mercadopago import create_preference
import decimal
import json
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from pedido.models import Pedido
from usuario.models import Cliente, EnderecoCliente
from services.dimona.api import get_frete
from .models import PagamentoMercadoPago


@login_required
def pagamento(request):
    if not 'carrinho' in request.session:
        # TODO: mandar mensagem no telegram avisando
        HttpResponseRedirect('/')

    uuid = request.session['carrinho']
    carrinho = Carrinho.objects.get(uuid=uuid)
    items = ItemCarrinho.objects.filter(carrinho=carrinho)
    valor_carrinho = 0

    user = request.user
    cliente = Cliente.objects.get(user=user)
    # TODO: aqui esta retornando somente um endereco
    enderecos = EnderecoCliente.objects.filter(cliente=cliente)[:1]


    item_data = []
    quantidade_total = 0
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
        quantidade_total = quantidade_total + item.quantidade
        valor_carrinho = (item.produto.preco_base *
                          item.quantidade) + valor_carrinho

    endereco = enderecos[0]
    cep = endereco.cep

    # monta o frete
    frete_items = get_frete(cep, quantidade_total)
    valor_frete = 5
    transportadora = ''
    delivery_method_id = 0
    if 'cotacao_frete' in request.session:
        delivery_method_id = int(request.session['cotacao_frete'])
        for frete in frete_items:
            if frete['delivery_method_id'] == delivery_method_id:
                valor_frete = frete['value']
                transportadora = frete['name']
                break
    else:
        for frete in frete_items:
            print('deve pegar o valor menor')

    payer = {
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

    valor_frete = round(float(valor_frete), 2)
    valor_total = round(valor_carrinho + decimal.Decimal(valor_frete), 2)

    # Cria o pedido
    pedido = Pedido.objects.create(
        valor_total=valor_total,
        valor_frete=valor_frete,
        valor_items=valor_carrinho,
        frete_id=delivery_method_id,
        frete_nome=transportadora,
        endereco_cliente=endereco
    )

    # monta urls de retorno
    back_urls = request.build_absolute_uri().replace('/pagamento/', '') + '/pedido/pedido_finalizado_mercado_pago'
    
    # junta o request pro mercado pago
    preference_data = {
        "back_urls": {
            "success": back_urls,
            "failure": back_urls,
            "pending": back_urls
        },
        "payer": payer,
        "auto_return": "approved",
        "items": item_data,
        "statement_descriptor": "LIKE_ESTAMPA",
        "external_reference": "LIKEESTAMPA-" + str(pedido.id),
        "installments": 10,
        "shipments": {
            "cost": float(valor_frete),
            "mode": "not_specified",
        }
    }

    # Cria a preferencia no mercado pago
    preference = create_preference(preference_data)

    # Atualiza informações na tabela de pagamento
    frase_padrao = 'PEDIDO_NAO_FINALIZADO'
    PagamentoMercadoPago.objects.create(
        pedido=pedido,
        mercado_pago_id=preference['id'],
        mercado_pago_status=frase_padrao,
        mercado_pago_status_detail=frase_padrao,
        payment_method_id=frase_padrao
    )

    # TODO: toda vez que da F5 ele cria um novo pedido. Validar isso
    request.session['mercado_pago_id'] = preference['id']

    context = {
        'items': items,
        'cliente': cliente,
        'valor_frete': valor_frete,
        'quantidade_item': len(items),
        'valor_carrinho': valor_carrinho,
        'valor_total': valor_total,
        'MERCADO_PAGO_PUBLIC_KEY': settings.MERCADO_PAGO_PUBLIC_KEY,
        'MERCADO_PAGO_PREFERENCE_ID': preference['id']
    }
    return render(request, 'pagamento/pagamento.html', context)
