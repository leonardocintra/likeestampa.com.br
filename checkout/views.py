from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from catalogo.models import Produto
from .models import Carrinho, Item
from .forms import ClienteForm


def carrinho(request):
    if not 'carrinho' in request.session:
        return HttpResponseRedirect(redirect_to='/')

    if request.method == 'POST':
        return redirect(reverse("pagamento:pagamento"))

    form = ClienteForm()
    uuid = request.session['carrinho']
    carrinho = Carrinho.objects.get(uuid=uuid)
    items = Item.objects.filter(carrinho=carrinho)

    context = {
        'form': form,
        'items': items,
        'quantidade_item': len(items),
        'peoplesoftURL': 'https://people-stage.herokuapp.com/v1/peoplesoft',
    }
    return render(request, 'checkout/carrinho.html', context)


def adicionar_item_carrinho(request, id):
    carrinho = Carrinho()
    if 'carrinho' in request.session:
        uuid = request.session['carrinho']
        carrinho = Carrinho.objects.get(uuid=uuid)
    else:
        carrinho.save()
        request.session['carrinho'] = str(carrinho.uuid)

    produto = Produto.objects.get(pk=id)
    item = Item.objects.filter(produto=produto, carrinho=carrinho)

    if item:
        Item.objects.filter(produto=produto, carrinho=carrinho).update(
            quantidade=item[0].quantidade + 1)
    else:
        Item(carrinho=carrinho, produto=produto, quantidade=1).save()

    return HttpResponseRedirect(redirect_to='/checkout/carrinho/')


def get_quantidade_items_carrinho(request):
    if 'carrinho' in request.session:
        uuid = request.session['carrinho']
        carrinho = Carrinho.objects.get(uuid=uuid)
        items = Item.objects.filter(carrinho=carrinho)
        return len(items)
    return 0
