# from django.utils.functional import cached_property
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from evento.models import criar_evento
from checkout.models import Carrinho, ItemCarrinho
from pedido.models import Pedido
from pedido.views import gerar_venda
from usuario.models import Cliente, EnderecoCliente
from services.mercadopago.mercadopago import create_preference, montar_payload_preference, get_payment
from services.dimona.api import get_frete
from services.telegram.api import enviar_mensagem
from .models import PagamentoMercadoPago
import decimal
import json


@login_required
def pagamento(request):
    if not 'carrinho' in request.session:
        # TODO: mandar mensagem no telegram avisando
        return HttpResponseRedirect('/')

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
    valor_frete = 10.0
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
        menor_valor = -1
        for frete in frete_items:
            if float(menor_valor) < float(0):
                menor_valor = float(frete['value'])

            if float(frete['value']) <= float(menor_valor):
                menor_valor = frete['value']

        valor_frete = menor_valor

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
    preference_data = montar_payload_preference(
        request, pedido.id, items, cliente, endereco, valor_frete)

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


def atualizar_pagamento(payment_id):
    obj_mp = get_payment(payment_id)

    if obj_mp['status'] == 'approved':
        PagamentoMercadoPago.objects.filter(payment_id=payment_id).update(
            mercado_pago_status=obj_mp['status'],
            mercado_pago_status_detail=obj_mp['status_detail'],
        )
        pagamento_mp = PagamentoMercadoPago.objects.get(payment_id=payment_id)
        gerar_venda(pagamento_mp=pagamento_mp)

    if obj_mp['status'] == 404:
        return JsonResponse({"pagamento": "nao-encontrado"}, status=200)

    if obj_mp['status'] != 'approved':
        return JsonResponse({"pagamento": "nao-aprovado"}, status=200)

    return JsonResponse({"pagamento": "aprovado"}, status=201)


@require_POST
@csrf_exempt
def mp_notifications(request):
    # Notificações do Mercado Pago IPN
    try:
        if request.GET.get('topic') == 'payment':
            payment_id = request.GET.get('id')
            enviar_mensagem(payment_id, 'IPN do Mercado pago')
            return atualizar_pagamento(payment_id)
        else:
            enviar_mensagem('Recebeu uma notificação IPN do mercado pago mas não foi um topic payment: {0} - ID: {1}'.format(
                request.GET.get('topic'), request.GET.get('id')), 'IPN do Mercado pago')
            return JsonResponse({"erro": "topico nao mapeado"}, status=200)
    except PagamentoMercadoPago.DoesNotExist:
        return JsonResponse({"payment": "not found"}, status=200)
    except print(0):
        enviar_mensagem('ERRO ao receber IPN: {0}'.format(str(request)))
        return JsonResponse({"payment": "not found"}, status=200)


@require_POST
@csrf_exempt
def webhook(request):
    # Notificações do Mercado Pago Webhook
    print('----- ENTREI -------------')
    print(str(request))
    payload = json.loads(request.body)
    payment_id = payload['id']

    if payload['live_mode']:
        enviar_mensagem(payload, payment_id, 'Webhook do Mercado pago')

    try:
        return atualizar_pagamento(payment_id)
    except PagamentoMercadoPago.DoesNotExist:
        enviar_mensagem('Pagamento não encontrato apos receber um Webhook do mercado pago',
                        payment_id, 'Webhook do Mercado pago')
        return JsonResponse({"foo": "bar"}, status=200)
    except:
        enviar_mensagem('ERRO ao receber Webhook: {0}'.format(request.body))
        return JsonResponse({"foo": "bar"}, status=200)
