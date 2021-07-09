from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.detail import DetailView

from checkout.models import Carrinho, ItemCarrinho
from pagamento.models import PagamentoMercadoPago
from services.mercadopago.mercadopago import get_preference, get_payment
from .models import Pedido, ItemPedido


@login_required
def pedido_finalizado_mercado_pago(request):
    if not 'mercado_pago_id' in request.session:
        pedido_id = int(request.session['pedido'])
        return redirect("pedido:pedido", pk=pedido_id)

    mercado_pago_id = request.session['mercado_pago_id']
    payment_id = request.GET.get('payment_id')

    preference = get_preference(mercado_pago_id)
    payment = get_payment(payment_id)

    # Atualiza os dados do mercado pago na tabela de pagamento
    PagamentoMercadoPago.objects.filter(
        mercado_pago_id=mercado_pago_id).update(
            transaction_amount=payment['transaction_amount'],
            installments=payment['installments'],
            payment_method_id=payment['payment_method_id'],
            mercado_pago_status=payment['status'],
            mercado_pago_status_detail=payment['status_detail'],
            payment_id=payment_id
    )
    pagamento_mp = PagamentoMercadoPago.objects.get(
        mercado_pago_id=mercado_pago_id)

    pago = False
    if pagamento_mp.mercado_pago_status == 'approved':
        pago = True

    # Atualiza os dados do pagamento no pedido (pago e o usuario)
    Pedido.objects.filter(pk=pagamento_mp.pedido.id).update(
        pago=pago,
        user_id = request.user.id
    )
    carrinho_uuid = request.session['carrinho']
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
            modelo=item.modelo,
            quantidade=item.quantidade
        )    
    del request.session['carrinho']
    del request.session['mercado_pago_id']
    # TODO: ver se deleta o carrinho e os items (registro do banco)

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
        context['items'] = items
        context['pagamento_mp'] = PagamentoMercadoPago.objects.get(pedido_id=self.object.pk)
        return context