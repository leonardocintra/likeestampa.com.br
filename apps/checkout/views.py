from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from core.constants import LEVEL_INFO
from services.dimona.api import get_frete
from services.telegram.api import enviar_mensagem
from usuario.models import Cliente, EnderecoCliente
from sentry_sdk import capture_message
from .forms import FreteForm
from .models import Carrinho, ItemCarrinho


def carrinho(request):
    cep = ''

    if request.method == 'POST':
        form = FreteForm(request.POST)
        # TODO: Alterar dados cadastrais ou incluir novo endereco
        if form.is_valid():
            request.session['cotacao_frete'] = form['delivery_method_id'].data
            enviar_mensagem(request.user.first_name, 'Carrinho de Compras', 'Algum cliente clicou no carrinho')
            return redirect(reverse("pagamento:pagamento"))

    valor_carrinho = 0
    items = None
    quantidade_item = 0
    if 'carrinho' in request.session:
        if 'calcular-frete' in request.POST:
            cep = request.POST['calcular-frete']
        uuid = request.session['carrinho']
        carrinho = Carrinho.objects.get(uuid=uuid)
        items = ItemCarrinho.objects.filter(carrinho=carrinho)

        """
        OBS: por enquanto o valor do item esta pegando do valor do modelo e nao do produto
        """
        for item in items:
            quantidade_item = quantidade_item + item.quantidade
            valor_carrinho = (item.modelo_produto.modelo.valor *
                              item.quantidade) + valor_carrinho

    form_frete = FreteForm()

    user = request.user
    cliente = None
    enderecos = None
    frete_items = {}

    if user.is_authenticated:
        cliente = Cliente.objects.get(user=user)
        enderecos = EnderecoCliente.objects.filter(cliente=cliente)

        for endereco in enderecos:
            if endereco.cep:
                cep = endereco.cep

    if cep != '' and items:
        frete_items = get_frete(cep, quantidade_item)
        if frete_items == []:
            frete_items = 'frete-nao-encontrado'

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
        capture_message('Sessions do basket id esta null ou não existe', level=LEVEL_INFO)
        return HttpResponseRedirect(redirect_to='/')

    uuid = request.session['carrinho']
    carrinho = Carrinho.objects.get(uuid=uuid)

    ItemCarrinho.objects.filter(pk=id, carrinho=carrinho).delete()
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
