import decimal
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from sentry_sdk import capture_exception, capture_message
from apps.core.constants import LEVEL_INFO

from apps.evento.models import criar_evento
from apps.checkout.models import Carrinho, ItemCarrinho
from apps.pagamento.business import atualizar_pagamento_mp
from apps.pedido.business import concluir_pedido
from apps.pedido.models import ItemPedido, Pedido
from apps.usuario.models import Cliente, EnderecoCliente
from services.mercadopago.mercadopago import create_preference, montar_payload_preference, get_payment, get_merchant_order, get_pagamento_by_external_reference
from services.dimona.api import get_frete
from services.telegram.api import enviar_mensagem
from .models import PagamentoMercadoPago


def _buscar_pedido_by_external_reference(external_reference):
    try:
        return Pedido.objects.get(uuid=external_reference)
    except Exception as e:
        capture_exception(e)
        return None


def _create_items_pedido(pedido, items):
    ItemPedido.objects.filter(pedido=pedido).delete()
    for item in items:
        ItemPedido.objects.create(
            pedido=pedido,
            produto=item.produto,
            cor=item.cor,
            tamanho=item.tamanho,
            modelo_produto=item.modelo_produto,
            quantidade=item.quantidade
        )


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
        valor_carrinho = (item.modelo_produto.modelo.valor *
                          item.quantidade) + valor_carrinho

    endereco = enderecos[0]
    cep = endereco.cep

    # monta o frete
    frete_items = get_frete(cep, quantidade_total)
    valor_frete = 15.0
    transportadora = 'DEFAULT-LIKEESTAMPA'
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

    # Cria o pedido. Se pedido ja existe, apenas faz update
    pedido = None
    if 'pedido_uuid' in request.session:
        try:
            pedido = Pedido.objects.get(uuid=request.session['pedido_uuid'])
            if pedido.session_ativa == False:
                del request.session['pedido_uuid']
            Pedido.objects.filter(
                uuid=request.session['pedido_uuid']).update(
                    user=user,
                    valor_total=valor_total,
                    valor_frete=valor_frete,
                    valor_items=valor_carrinho,
                    frete_id=delivery_method_id,
                    frete_nome=transportadora,
                    endereco_cliente=endereco,
            )
        except Exception as e:
            capture_exception(e)
            pedido = None

    if pedido is None:
        pedido = Pedido.objects.create(
            user=user,
            valor_total=valor_total,
            valor_frete=valor_frete,
            valor_items=valor_carrinho,
            frete_id=delivery_method_id,
            frete_nome=transportadora,
            endereco_cliente=endereco,
            session_ativa=True
        )
        # Cria o evento inicial
        criar_evento(1, pedido)

    _create_items_pedido(pedido, items)
    capture_message('Pedido: ' + str(pedido.id), level=LEVEL_INFO)
    request.session['pedido_uuid'] = str(pedido.uuid)

    # Monta o payload para enviar pro mercado pago
    preference_data = montar_payload_preference(
        request, pedido.uuid, items, cliente, endereco, valor_frete)

    # Cria a preferencia no mercado pago
    preference = create_preference(preference_data)
    preference_id = preference['id']

    # Atualiza informações na tabela de pagamento
    FRASE_PADRAO = 'PEDIDO_NAO_FINALIZADO'
    PagamentoMercadoPago.objects.filter(pedido=pedido).delete()
    PagamentoMercadoPago.objects.create(
        pedido=pedido,
        mercado_pago_id=preference_id,
        mercado_pago_status=FRASE_PADRAO,
        mercado_pago_status_detail=FRASE_PADRAO,
        payment_method_id=FRASE_PADRAO
    )
    Carrinho.objects.filter(uuid=uuid).update(pedido=pedido)
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
def mp_notifications(request):
    """
        Mercado Pago IPN notificacoes
        -Obs: Mercado Pago IPN não funciona em STAGE, entao tem que fazer os POST na mão.
              O problema é que a notificação chega num grupo do telegram. Se quiser acesso 
              precisa entrar em contato com leonardo.ncintra@outlook.com
    """

    try:
        if request.GET.get('topic') != 'payment' and request.GET.get('topic') != 'merchant_order':
            enviar_mensagem('Recebeu uma notificação IPN do mercado pago mas não foi um topic mapeado: {0} - ID: {1}'.format(
                request.GET.get('topic'), request.GET.get('id')), 'IPN do Mercado pago')
            return JsonResponse({"erro": "topico nao mapeado"}, status=200)

        payment_id = request.GET.get('id')
        pedido = None

        if request.GET.get('topic') == 'merchant_order':
            merchant_order = get_merchant_order(request.GET.get('id'))
            enviar_mensagem(
                merchant_order['id'], 'Merchant Order', 'POST IPN MERCADO PAGO')

            external_reference = merchant_order['external_reference']
            pedido = _buscar_pedido_by_external_reference(external_reference)
            if not pedido:
                capture_message('Pedido não encontrado. External Reference: ' +
                                str(external_reference), level=LEVEL_INFO)
                enviar_mensagem(external_reference,
                                'Pedido não encontrado', 'External Reference')
                return JsonResponse({"pedido": "pedido-nao-encontrado"}, status=200)

            datas = get_pagamento_by_external_reference(external_reference)

            try:
                # TODO: as vezes pode ter mais de um resuts. Entao fazer um loop para pegar sempre o ultimo
                payment_id = datas['results'][0]['id']
            except Exception as e:
                capture_exception(e)
                return JsonResponse({"payment_id": "payment_id-nao-encontrado"}, status=200)

            Pedido.objects.filter(uuid=external_reference).update(
                session_ativa=False)
            PagamentoMercadoPago.objects.filter(
                pedido=pedido).update(payment_id=payment_id)


        payment = get_payment(payment_id)
        if payment['status'] == 404:
            return JsonResponse({"pagamento": "nao-encontrado"}, status=200)

        atualizar_pagamento_mp(payment)
        try:
            if pedido is None:
                pedido = _buscar_pedido_by_external_reference(
                    payment['external_reference'])
            concluir_pedido(pedido, payment_id)
        except Exception as e:
            capture_exception(e)
            enviar_mensagem('Erro ao concluir_pedido. Erro: {0}'.format(e))
            return JsonResponse({"pagamento": "ocorreu um erro no concluir-pedido."}, status=201)

        return JsonResponse({"pagamento": "dado-recebido"}, status=201)

    except PagamentoMercadoPago.DoesNotExist:
        return JsonResponse({"payment": "pagamento não encontrado"}, status=200)
    except Exception as ex:
        capture_exception(ex)
        enviar_mensagem(
            'ERRO ao receber IPN: {0} - {1}'.format(str(request), ex))
        return JsonResponse({"payment": "ocorreu um excetipon ao processar"}, status=200)


@require_POST
@csrf_exempt
def webhook(request):
    # Notificações do Mercado Pago Webhook
    # Repetir mesma regra do IPN
    enviar_mensagem('MENSAGEM Webhook: {0}'.format(str(request)))
    return JsonResponse({"pagamento": "webhook-nao-configurado"}, status=200)
