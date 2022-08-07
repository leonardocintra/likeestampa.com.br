from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from sentry_sdk import capture_exception

from apps.checkout.models import Carrinho
from evento.models import EventoPedido
from pagamento.models import PagamentoMercadoPago
from services.dimona.api import get_tracking_url
from services.telegram.api import enviar_mensagem
from .models import Pedido, ItemPedido

@login_required
def pedido_finalizado_mercado_pago(request):
    if not 'mercado_pago_id' in request.session:
        pedido_id = int(request.session['pedido'])
        return redirect("pedido:pedido", pk=pedido_id)

    # TODO: isso aqui pode ser null ?
    carrinho_uuid = request.session['carrinho']

    mercado_pago_id = request.session['mercado_pago_id']

    pagamento_mp = PagamentoMercadoPago.objects.get(
        mercado_pago_id=mercado_pago_id)

    del request.session['carrinho']
    del request.session['mercado_pago_id']
    del request.session['pedido_uuid']
    Carrinho.objects.filter(uuid=carrinho_uuid).delete()
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
        tracking = get_tracking_url(self.object.pedido_seller)
        try:
            url_rastreio = tracking['tracking_url']
        except Exception as e:
            capture_exception(e)
            enviar_mensagem('Erro ao buscar a URL de rastreio do pedido ' + str(self.object))
            url_rastreio = ''
        

        context['url_rastreio'] = url_rastreio
        context['eventos'] = eventos
        context['items'] = items
        context['pagamento_mp'] = PagamentoMercadoPago.objects.get(
            pedido_id=self.object.pk)
        return context
