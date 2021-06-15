from django.conf import settings
from django.shortcuts import render
from checkout.models import Carrinho, Item
from services.mercadopago import mercadopago
from services.peoplesoft.peoplesoft import buscar_cliente_by_id


def pagamento(request):

    if request.method == 'POST':
        mercadopago.mercado_pago(request)

    if 'carrinho' in request.session:
        uuid = request.session['carrinho']
        carrinho = Carrinho.objects.get(uuid=uuid)
        items = Item.objects.filter(carrinho=carrinho)
    
    if 'cliente_id' in request.session:
        cliente = buscar_cliente_by_id(request.session['cliente_id'])
        cliente = cliente['records'][0]

    context = {
        'items': items,
        'cliente': cliente,
        'quantidade_item': len(items),
        'MERCADO_PAGO_PUBLIC_KEY': settings.MERCADO_PAGO_PUBLIC_KEY,
    }
    return render(request, 'pagamento/pagamento.html', context)


def process_payment(request):
    print('vai se foder mercado pago')
