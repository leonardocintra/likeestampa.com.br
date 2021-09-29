from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.detail import DetailView

from checkout.models import Carrinho, ItemCarrinho
from evento.models import EventoPedido, criar_evento
from pagamento.models import PagamentoMercadoPago
from pagamento.business import atualizar_pagamento_mp
from services.mercadopago.mercadopago import get_payment, confirma_pagamento
from services.dimona.api import create_order, get_tracking_url, create_payload_order
from services.telegram.api import enviar_mensagem
from usuario.models import Cliente, EnderecoCliente
from .models import Pedido, ItemPedido
from .email import envia_email


def gerar_venda(pagamento_mp):
    try:
        enviar_mensagem('Pedido {0} gerando compra dimona ...'.format(str(pagamento_mp.pedido.id)), 'Pedido sendo realizado', str(pagamento_mp.pedido.id))
        pedido = Pedido.objects.get(pk=pagamento_mp.pedido.id)
        dimona = None

        if pedido.pago:
            enviar_mensagem('Pedido {0} ja foi pago e gerado!'.format(str(pagamento_mp.pedido.id)), 'Pedido ja consta pago', str(pagamento_mp.pedido.id))
        else:
            dimona = create_order(pedido.request_seller)
            dimona = dimona['order']

            # Atualiza os dados do pagamento no pedido (pago e o usuario)
            Pedido.objects.filter(pk=pagamento_mp.pedido.id).update(
                pago=True,
                pedido_seller=dimona
            )
            enviar_mensagem('Pedido {0} - Dimona: {1} criado com sucesso!'.format(str(pagamento_mp.pedido.id), dimona), 'Pedido realizado', str(pagamento_mp.pedido.id))
    except:
        enviar_mensagem('Erro ao gerar venda')
        enviar_mensagem('Pedido {0} - ERRO'.format(str(pagamento_mp.pedido.id)), 'ERRO', str(pagamento_mp.pedido.id))


@login_required
def pedido_finalizado_mercado_pago(request):
    if not 'mercado_pago_id' in request.session:
        pedido_id = int(request.session['pedido'])
        return redirect("pedido:pedido", pk=pedido_id)

    # TODO: isso aqui pode ser null ?
    carrinho_uuid = request.session['carrinho']

    mercado_pago_id = request.session['mercado_pago_id']
    payment_id = request.GET.get('payment_id')
    payment = get_payment(payment_id)

    atualizar_pagamento_mp(payment, mercado_pago_id, payment_id)

    pagamento_mp = PagamentoMercadoPago.objects.get(
        mercado_pago_id=mercado_pago_id)

    Carrinho.objects.filter(uuid=carrinho_uuid).update(
        abandonado=False, finalizado=True)
    carrinho = Carrinho.objects.get(uuid=carrinho_uuid)
    items = ItemCarrinho.objects.filter(carrinho=carrinho)

    for item in items:
        ItemPedido.objects.create(
            pedido=pagamento_mp.pedido,
            produto=item.produto,
            cor=item.cor,
            tamanho=item.tamanho,
            modelo_produto=item.modelo_produto,
            quantidade=item.quantidade
        )

    pedido = Pedido.objects.get(pk=pagamento_mp.pedido.id)
    pago = False
    user = request.user
    cliente = Cliente.objects.get(user=user)
    enderecos = EnderecoCliente.objects.filter(cliente=cliente)

    create_payload_order(pagamento_mp.pedido.id, cliente,
                         enderecos[0], items, pedido.frete_id)
    if pagamento_mp.mercado_pago_status == 'approved' and confirma_pagamento(payment_id):
        pago = True
        criar_evento(2, pedido)  # Pedido Pago
        criar_evento(3, pedido)  # Pedido em producao
        gerar_venda(pagamento_mp)

    if not pago:
        criar_evento(6, pedido)  # Aguardando pagamento

    envia_email(cliente, pedido.id, pago, items)

    del request.session['carrinho']
    del request.session['mercado_pago_id']
    Carrinho.objects.filter(uuid=carrinho_uuid).delete()
    ItemCarrinho.objects.filter(carrinho=carrinho).delete()

    return redirect("pedido:pedido", pk=pagamento_mp.pedido.id)


class PedidoDetailView(LoginRequiredMixin, DetailView):
    template_name = 'pedido/pedido.html'
    model = Pedido

    def get(self, request, *args, **kwargs):
        try:
            pedido = Pedido.objects.get(pk=self.kwargs['pk'])
        except Pedido.DoesNotExist:
            return redirect("usuario:cliente")

        # Aqui nao deixa o usuario entrar o pedido que nao for ele que esta conectado
        if self.request.user.id != pedido.user_id:
            return redirect("usuario:cliente")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = ItemPedido.objects.filter(pedido=self.object)
        eventos = EventoPedido.objects.filter(pedido=self.object)
        url_rastreio = get_tracking_url(self.object.pedido_seller)[
            'tracking_url']

        context['url_rastreio'] = url_rastreio
        context['eventos'] = eventos
        context['items'] = items
        context['pagamento_mp'] = PagamentoMercadoPago.objects.get(
            pedido_id=self.object.pk)
        return context
