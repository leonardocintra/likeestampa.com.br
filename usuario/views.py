from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Cliente


@login_required
def cliente(request):
    user = request.user
    cliente = Cliente.objects.get(user=user)
    context = {
        'cliente': cliente
    }
    return render(request, "usuario/profile.html", context)
