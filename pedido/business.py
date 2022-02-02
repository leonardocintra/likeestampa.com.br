from checkout.models import Carrinho
from evento.models import criar_evento
from pagamento.models import PagamentoMercadoPago
from pedido.email import envia_email
from pedido.models import ItemPedido, Pedido
from services.dimona.api import create_order, create_payload_order
from services.mercadopago.mercadopago import confirma_pagamento
from services.telegram.api import enviar_mensagem
from usuario.models import Cliente, EnderecoCliente


def _gerar_venda(pagamento_mp):
    # TODO: esta dando erro aqui para boletos
    try:
        enviar_mensagem('Pedido {0} gerando compra dimona ...'.format(str(
            pagamento_mp.pedido.id)), 'Pedido sendo realizado', str(pagamento_mp.pedido.id))
        dimona = None
        pedido = Pedido.objects.get(pk=pagamento_mp.pedido.id)
        dimona = create_order(pedido.request_seller)
        dimona = dimona['order']

        # Atualiza os dados do pagamento no pedido (pago e o usuario)
        Pedido.objects.filter(pk=pagamento_mp.pedido.id).update(
            pago=True,
            pedido_seller=dimona
        )
        enviar_mensagem('Pedido {0} - Dimona: {1} criado com sucesso!'.format(str(
            pagamento_mp.pedido.id), dimona), 'Pedido realizado', str(pagamento_mp.pedido.id))
    except Exception as e:
        enviar_mensagem('Erro ao gerar venda: ' + str(e))
        enviar_mensagem(
            'Pedido {0} - ERRO'.format(str(pagamento_mp.pedido.id)), 'ERRO', str(pagamento_mp.pedido.id))


def concluir_pedido(pedido, payment_id):
    # Aqui finalizamos o pedido (indepentende de estar pago)
    pago = False
    cliente = Cliente.objects.get(user=pedido.user)
    enderecos = EnderecoCliente.objects.filter(cliente=cliente)
    items = ItemPedido.objects.filter(pedido=pedido)
    pagamento = PagamentoMercadoPago.objects.get(pedido=pedido)
    Carrinho.objects.filter(pedido=pedido).delete()
    
    if not pedido.pedido_seller:
        # DIMONA: cria o payload (request)
        create_payload_order(pedido.id, cliente,
                            enderecos[0], items, pedido.frete_id)

    if pagamento.mercado_pago_status == 'approved' and confirma_pagamento(payment_id):
        pago = True
        criar_evento(2, pedido)  # Pedido Pago
        criar_evento(3, pedido)  # Pedido em producao
        _gerar_venda(pagamento)
    else:
        criar_evento(6, pedido)  # Aguardando pagamento
    envia_email(cliente, pedido.id, pago, items)
