from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
# from django.utils.functional import cached_property
from evento.models import EventoPedido, criar_evento
from checkout.models import Carrinho, ItemCarrinho
from pedido.models import Pedido
from usuario.models import Cliente, EnderecoCliente
from services.mercadopago.mercadopago import create_preference, montar_payload_preference
from services.dimona.api import get_frete
from .models import PagamentoMercadoPago, PagamentoMercadoPagoWebhook
import decimal
import json


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

    quantidade_total = 0
    for item in items:
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

    valor_frete = round(float(valor_frete), 2)
    valor_total = round(valor_carrinho + decimal.Decimal(valor_frete), 2)

    # Cria o pedido
    pedido = Pedido.objects.create(
        user=user,
        valor_total=valor_total,
        valor_frete=valor_frete,
        valor_items=valor_carrinho,
        frete_id=delivery_method_id,
        frete_nome=transportadora,
        endereco_cliente=endereco
    )

    # Cria o evento inicial
    criar_evento(1, pedido)

    # Monta o payload para enviar pro mercado pago
    preference_data = montar_payload_preference(request, pedido.id, items, cliente, endereco, valor_frete)

    # Cria a preferencia no mercado pago
    preference = create_preference(preference_data)
    preference_id = preference['id']

    # Atualiza informações na tabela de pagamento
    frase_padrao = 'PEDIDO_NAO_FINALIZADO'
    PagamentoMercadoPago.objects.create(
        pedido=pedido,
        mercado_pago_id=preference_id,
        mercado_pago_status=frase_padrao,
        mercado_pago_status_detail=frase_padrao,
        payment_method_id=frase_padrao
    )

    # TODO: toda vez que da F5 ele cria um novo pedido. Validar isso
    request.session['mercado_pago_id'] = preference_id

    context = {
        'items': items,
        'cliente': cliente,
        'valor_frete': valor_frete,
        'quantidade_item': len(items),
        'valor_carrinho': valor_carrinho,
        'valor_total': valor_total,
        'MERCADO_PAGO_PUBLIC_KEY': settings.MERCADO_PAGO_PUBLIC_KEY,
        'MERCADO_PAGO_PREFERENCE_ID': preference_id
    }
    return render(request, 'pagamento/pagamento.html', context)


@require_POST
@csrf_exempt
def webhook(request):
    print('ok - webhook mercado pago!')
    return JsonResponse({"foo": "bar"}, status=201)