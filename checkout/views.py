from django.shortcuts import render
from django.conf import settings


def carrinho(request):
    context = {
        'MERCADO_PAGO_PUBLIC_KEY': settings.MERCADO_PAGO_PUBLIC_KEY
    }
    return render(request, 'checkout/carrinho.html', context)
