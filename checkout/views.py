from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from catalogo.models import Produto
from .models import Carrinho, Item
from .forms import ClienteForm
from services.peoplesoft.peoplesoft import cadastrar_cliente, buscar_cliente_by_id


def carrinho(request):
    if not 'carrinho' in request.session:
        return HttpResponseRedirect(redirect_to='/')

    if request.method == 'POST':
        form = ClienteForm(request.POST)
        cliente_id = cadastrar_cliente(form.data)
        request.session['cliente_id'] = str(cliente_id)
        if form.is_valid():
            return redirect(reverse("pagamento:pagamento"))
        print(form.errors)

    uuid = request.session['carrinho']
    carrinho = Carrinho.objects.get(uuid=uuid)
    items = Item.objects.filter(carrinho=carrinho)

    form = ClienteForm()
    if 'cliente_id' in request.session:
        cliente = buscar_cliente_by_id(request.session['cliente_id'])
        cliente = cliente['records'][0]
        endereco = cliente['enderecos'][0]
        form.fields['cpf'].initial = cliente['cpf']
        form.fields['nome'].initial = cliente['nome']
        form.fields['email'].initial = cliente['email']
        form.fields['cep'].initial = endereco['cep']
        form.fields['cidade'].initial = endereco['cidade']
        form.fields['uf'].initial = endereco['uf']
        form.fields['numero'].initial = endereco['numero']
        form.fields['bairro'].initial = endereco['bairro']
        form.fields['endereco'].initial = endereco['endereco']
        form.fields['complemento'].initial = endereco['complemento']
        form.fields['referencia'].initial = endereco['referencia']

        form.fields['nome'].widget.attrs['readonly'] = True
        form.fields['email'].widget.attrs['readonly'] = True
        form.fields['cep'].widget.attrs['readonly'] = True
        form.fields['cidade'].widget.attrs['readonly'] = True
        form.fields['uf'].widget.attrs['readonly'] = True
        form.fields['numero'].widget.attrs['readonly'] = True
        form.fields['bairro'].widget.attrs['readonly'] = True
        form.fields['endereco'].widget.attrs['readonly'] = True
        form.fields['complemento'].widget.attrs['readonly'] = True
        form.fields['referencia'].widget.attrs['readonly'] = True

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


def excluir_item_carrinho(request, id):
    if not 'carrinho' in request.session:
        return HttpResponseRedirect(redirect_to='/')

    uuid = request.session['carrinho']
    carrinho = Carrinho.objects.get(uuid=uuid)

    item = Item.objects.filter(pk=id, carrinho=carrinho).delete()
    return HttpResponseRedirect(redirect_to='/checkout/carrinho/')


def get_quantidade_items_carrinho(request):
    if 'carrinho' in request.session:
        uuid = request.session['carrinho']
        carrinho = Carrinho.objects.get(uuid=uuid)
        items = Item.objects.filter(carrinho=carrinho)
        return len(items)
    return 0
