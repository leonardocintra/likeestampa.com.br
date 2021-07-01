from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from checkout.forms import ClienteForm
from pedido.models import Pedido
from .business import get_cliente_data_form
from .models import Cliente
from django.http.response import HttpResponseRedirect


@login_required
def cliente(request):
    user = request.user
    if user.is_staff:
        return HttpResponseRedirect('/')
    cliente = Cliente.objects.get(user=user)
    request.session['cliente_id'] = cliente.peoplesoft_id
    form = get_cliente_data_form(request)
    pedidos = Pedido.objects.filter(peoplesoft_pessoa_id=cliente.peoplesoft_id)
    context = {
        'cliente': cliente,
        'form': form,
        'pedidos': pedidos
    }
    return render(request, "usuario/profile.html", context)
