from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView
from services.mercadopago.mercadopago import get_preference, get_payment
from pagamento.models import PagamentoMercadoPago
from pedido.models import Pedido
from .models import Pedido
from checkout.models import Carrinho


class PedidoDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'pedido/pedido.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mercado_pago_id = self.request.session['mercado_pago_id']
        payment_id = self.request.GET.get('payment_id')

        preference = get_preference(mercado_pago_id)
        payment = get_payment(payment_id)

        mp = PagamentoMercadoPago.objects.filter(
            mercado_pago_id=mercado_pago_id).update(
                transaction_amount=payment['transaction_amount'],
                installments=payment['installments'],
                payment_method_id=payment['payment_method_id'],
                mercado_pago_status=payment['status'],
                mercado_pago_status_detail=payment['status_detail'],
                payment_id=payment_id
        )
        pagamento_mp = PagamentoMercadoPago.objects.get(pk=mp)

        ped = Pedido.objects.filter(pk=pagamento_mp.pedido).update(pago=True)
        pedido = Pedido.objects.get(pk=ped)
        carrinho_uuid = self.request.session['carrinho']
        Carrinho.objects.filter(uuid=carrinho_uuid).update(
            abandonado=False, finalizado=True)
        del self.request.session['carrinho']
        del self.request.session['mercado_pago_id']

        context['pedido'] = pedido
        return context
