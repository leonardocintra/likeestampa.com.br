from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from catalogo.models import Produto
from usuario.business import get_cliente_data_form
from services.dimona.api import get_frete
from .models import Carrinho, ItemCarrinho
from .forms import ClienteForm


def carrinho(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        # TODO: Alterar dados cadastrais ou incluir novo endereco
        if form.is_valid():
            return redirect(reverse("pagamento:pagamento"))
        print(form.errors)

    valor_carrinho = 0
    items = None
    quantidade_item = 0
    if 'carrinho' in request.session:
        uuid = request.session['carrinho']
        carrinho = Carrinho.objects.get(uuid=uuid)
        items = ItemCarrinho.objects.filter(carrinho=carrinho)
    
        for item in items:
            quantidade_item = quantidade_item + item.quantidade
            valor_carrinho = (item.produto.preco_base *
                            item.quantidade) + valor_carrinho

    form = get_cliente_data_form(request)

    frete_items = {}
    if items:
        frete_items = get_frete(form['cep'].initial, quantidade_item)

    context = {
        'form': form,
        'items': items,
        'frete_items': frete_items,
        'quantidade_item': quantidade_item,
        'valor_carrinho': valor_carrinho,
        'peoplesoftURL': settings.PEOPLE_SOFT_API,
    }
    return render(request, 'checkout/carrinho.html', context)


def excluir_item_carrinho(request, id):
    if not 'carrinho' in request.session:
        return HttpResponseRedirect(redirect_to='/')

    uuid = request.session['carrinho']
    carrinho = Carrinho.objects.get(uuid=uuid)

    item = ItemCarrinho.objects.filter(pk=id, carrinho=carrinho).delete()
    return HttpResponseRedirect(redirect_to='/checkout/carrinho/')


def get_quantidade_items_carrinho(request):
    if not 'carrinho' in request.session:
        return 0

    try:
        uuid = request.session['carrinho']
        carrinho = Carrinho.objects.get(uuid=uuid)
        items = ItemCarrinho.objects.filter(carrinho=carrinho)
    except Carrinho.DoesNotExist:
        del request.session['carrinho']
        return 0

    return len(items)
