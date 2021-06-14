from django.conf import settings
from django.shortcuts import render
from checkout.models import Carrinho, Item
from services.mercadopago import mercadopago


def pagamento(request):

    if request.method == 'POST':
        mercadopago.mercado_pago(request)

    if 'carrinho' in request.session:
        uuid = request.session['carrinho']
        carrinho = Carrinho.objects.get(uuid=uuid)
        items = Item.objects.filter(carrinho=carrinho)

    context = {
        'items': items,
        'quantidade_item': len(items),
        'MERCADO_PAGO_PUBLIC_KEY': settings.MERCADO_PAGO_PUBLIC_KEY,
    }
    return render(request, 'pagamento/pagamento.html', context)


def process_payment(request):
    print('vai se foder mercado pago')
