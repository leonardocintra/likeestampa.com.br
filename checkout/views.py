from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from catalogo.models import Produto
from services.dimona.api import get_frete
from services.telegram.api import enviar_mensagem
from usuario.forms import ClienteForm
from usuario.models import Cliente, EnderecoCliente
from .forms import FreteForm
from .models import Carrinho, ItemCarrinho


def carrinho(request):
    if request.method == 'POST':
        form = FreteForm(request.POST)
        enviar_mensagem('Cliente novo na área', 'Carrinho de Compras', 'Algum cliente clicou no carrinho')
        request.session['cotacao_frete'] = form['delivery_method_id'].data
        # TODO: Alterar dados cadastrais ou incluir novo endereco
        if form.is_valid():
            return redirect(reverse("pagamento:pagamento"))

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

    form_frete = FreteForm()

    user = request.user
    cliente = None
    enderecos = None
    cep = ''
    frete_items = {}

    if user.is_authenticated:
        cliente = Cliente.objects.get(user=user)
        enderecos = EnderecoCliente.objects.filter(cliente=cliente)

        for endereco in enderecos:
            if endereco.cep:
                cep = endereco.cep

        if items:
            frete_items = get_frete(cep, quantidade_item)

    context = {
        'form_frete': form_frete,
        'cep_padrao': cep,
        'items': items,
        'frete_items': frete_items,
        'quantidade_item': quantidade_item,
        'valor_carrinho': valor_carrinho,
        'cliente': cliente,
        'enderecos': enderecos
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
