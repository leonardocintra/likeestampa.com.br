from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.views.generic.edit import UpdateView
from pedido.models import Pedido
from .models import Cliente, EnderecoCliente


@login_required
def cliente(request):
    user = request.user
    if user.is_staff:
        return HttpResponseRedirect('/')
    cliente = Cliente.objects.get(user=user)
    enderecos = EnderecoCliente.objects.filter(cliente=cliente)
    pedidos = Pedido.objects.filter(endereco_cliente__in=enderecos)
    context = {
        'cliente': cliente,
        'enderecos': enderecos,
        'pedidos': pedidos
    }
    return render(request, "usuario/profile.html", context)


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    template_name = "usuario/update_cliente.html"
    fields = ('cpf', 'telefone', )


cliente_update = ClienteUpdateView.as_view()

