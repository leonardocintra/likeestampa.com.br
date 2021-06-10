from django.http import HttpResponseRedirect
from django.shortcuts import render
from catalogo.models import Produto
from .models import Carrinho, Item


def carrinho(request):
    if 'carrinho' in request.session:
        uuid = request.session['carrinho']
        carrinho = Carrinho.objects.get(uuid=uuid)
        items = Item.objects.filter(carrinho=carrinho)

    context = {
        'items': items,
        'quantidade_item': len(items),
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
    

