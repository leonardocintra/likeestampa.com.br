from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from checkout.forms import ClienteForm
from .business import get_cliente_data_form
from .models import Cliente


@login_required
def cliente(request):
    user = request.user
    cliente = Cliente.objects.get(user=user)
    request.session['cliente_id'] = cliente.peoplesoft_id
    form = get_cliente_data_form(request)
    context = {
        'cliente': cliente,
        'form': form
    }
    return render(request, "usuario/profile.html", context)
