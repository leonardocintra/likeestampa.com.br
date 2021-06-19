from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from catalogo.models import Produto
from usuario.business import get_cliente_data_form
from .models import Carrinho, Item
from .forms import ClienteForm


def carrinho(request):
    if not 'carrinho' in request.session:
        return HttpResponseRedirect(redirect_to='/')

    if request.method == 'POST':
        form = ClienteForm(request.POST)
        # TODO: Alterar dados cadastrais ou incluir novo endereco
        if form.is_valid():
            return redirect(reverse("pagamento:pagamento"))
        print(form.errors)

    uuid = request.session['carrinho']
    carrinho = Carrinho.objects.get(uuid=uuid)
    items = Item.objects.filter(carrinho=carrinho)

    form = get_cliente_data_form(request)

    valor_carrinho = 0
    for item in items:
        valor_carrinho = (item.produto.preco_base *
                          item.quantidade) + valor_carrinho

    context = {
        'form': form,
        'items': items,
        'quantidade_item': len(items),
        'valor_carrinho': valor_carrinho,
        'peoplesoftURL': 'https://people-stage.herokuapp.com/v1/peoplesoft',
    }
    return render(request, 'checkout/carrinho.html', context)


def excluir_item_carrinho(request, id):
    if not 'carrinho' in request.session:
        return HttpResponseRedirect(redirect_to='/')

    uuid = request.session['carrinho']
    carrinho = Carrinho.objects.get(uuid=uuid)

    item = Item.objects.filter(pk=id, carrinho=carrinho).delete()
    return HttpResponseRedirect(redirect_to='/checkout/carrinho/')


def get_quantidade_items_carrinho(request):
    if not 'carrinho' in request.session:
        return 0

    uuid = request.session['carrinho']
    carrinho = Carrinho.objects.get(uuid=uuid)
    items = Item.objects.filter(carrinho=carrinho)
    return len(items)
