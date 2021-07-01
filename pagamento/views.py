from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
# from django.utils.functional import cached_property
from checkout.models import Carrinho, ItemCarrinho
from services.mercadopago.mercadopago import create_preference
from services.peoplesoft.peoplesoft import buscar_cliente_by_id
from django.http import HttpResponse
from pedido.models import Pedido
from .models import PagamentoMercadoPago
import json


@login_required
def pagamento(request):
    if not 'carrinho' in request.session:
        pass  # TODO: mandar mensagem no telegram avisando
    
    if 'cliente_id' in request.session:
        pass  # TODO: mandar mensagem no telegram avisando

    uuid = request.session['carrinho']
    carrinho = Carrinho.objects.get(uuid=uuid)
    items = ItemCarrinho.objects.filter(carrinho=carrinho)
    valor_carrinho = 0

    cliente = buscar_cliente_by_id(request.session['cliente_id'])
    cliente = cliente['records'][0]
    endereco = cliente['enderecos'][0]

    payer = {
        "name": cliente['nome'],
        "surname": "SOBRENOME NO NOME",
        "email": cliente['email'],
        "identification": {
            "type": "CPF",
            "number": cliente['cpf']
        },
        "address": {
            "street_name": endereco['endereco'],
            "street_number": endereco['numero'],
            "zip_code": endereco['cep']
        }
    }

    item_data = []
    for item in items:
        item_data.append({
            "id": item.produto.slug,
            "title": item.produto.nome,
            "picture_url": "https://res.cloudinary.com/leonardocintra/image/upload/" + str(item.produto.imagem_principal) + ".jpg",
            # "description": item.produto.descricao,
            "category_id": item.produto.subcategoria.slug,
            "quantity": item.quantidade,
            "unit_price": float(item.produto.preco_base)
        })
        valor_carrinho = (item.produto.preco_base *
                          item.quantidade) + valor_carrinho

    back_urls = request.build_absolute_uri().replace('/pagamento/', '') + '/pedido/pedido_finalizado_mercado_pago'
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
        "external_reference": "CAMISETA_DA_HORA",
        "installments": 10
    }

    preference = create_preference(preference_data)

    pedido = Pedido.objects.create(
        cpf=cliente['cpf'],
        peoplesoft_pessoa_id=cliente['id'],
        peoplesoft_endereco_id=endereco['id'],
        valor_total=valor_carrinho
    )
    
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
        'quantidade_item': len(items),
        'valor_carrinho': valor_carrinho,
        'MERCADO_PAGO_PUBLIC_KEY': settings.MERCADO_PAGO_PUBLIC_KEY,
        'MERCADO_PAGO_PREFERENCE_ID': preference['id']
    }
    return render(request, 'pagamento/pagamento.html', context)
