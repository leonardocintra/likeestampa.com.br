from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic.base import TemplateView

from catalogo.models import Produto, SubCategoria
from checkout.views import get_quantidade_items_carrinho


def index(request):
    # Pagina inicial - Listagem dos ultimos lançamentos
    produtos = __get_produtos(request=request)
    subcategorias = SubCategoria.get_subcategorias_ativas()
    quantidade_item = get_quantidade_items_carrinho(request)
    page_obj = __get_page_obj(request, produtos)

    context = {
        'produtos': produtos,
        'page_obj': page_obj,
        'subcategorias': subcategorias,
        'quantidade_item': quantidade_item,
    }

    return render(request, 'index.html', context)


def __get_page_obj(request, produtos):
    paginator = Paginator(produtos, 32)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def __get_produtos(request):
    produtos = Produto.get_produtos_ativos_e_tela_inicial_true()
    q = request.GET.get('q', '')
    if q:
        return produtos.filter(nome__icontains=q).exclude(
            ativo=False).exclude(mostrar_tela_inicial=False)
    return produtos


class AboutView(TemplateView):
    template_name = "about.html"


class TrocaCancelamentoView(TemplateView):
    template_name = "troca-e-cancelamento.html"


class TermosDeUsoView(TemplateView):
    template_name = "termos-de-uso.html"
