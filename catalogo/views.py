from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from checkout.views import get_quantidade_items_carrinho
from checkout.models import Carrinho, ItemCarrinho
from .forms import ProdutoDetalheForm
from .models import Cor, Produto, ProdutoImagem, SubCategoria, ModeloProduto, Tamanho, TamanhoModelo


def lista_por_subcategoria(request, slug):
    """ Lista os produtos baseado na categoria selecionada """

    subcategorias = SubCategoria.get_subcategorias_ativas()
    sub_categoria_selecionada = get_object_or_404(subcategorias, slug=slug)
    produtos = Produto.get_produtos_ativos().filter(
        subcategoria__slug=slug)
    page_obj = __get_page_obj(request, produtos)

    context = {
        'page_obj': page_obj,
        'subcategorias': subcategorias,
        'sub_categoria_selecionada': sub_categoria_selecionada,
    }
    return render(request, 'catalogo/list_by_categoria.html', context)


def produto(request, slug):
    """ Pagina de detalhes do produto """

    produto = Produto.get_produto_by_slug(slug)

    if request.method == 'POST':
        form = ProdutoDetalheForm(request.POST)
        __adicionar_item_carrinho(request, produto, form.data['modelo'],
                                  form.data['cor'], form.data['tamanho'], form.data['quantidade'])
        return redirect(reverse("checkout:carrinho"))

    imagens = ProdutoImagem.objects.filter(produto=produto)
    # Adiciona no mockup a imagem principal (pelo menos a imagem 0)

    mockups = __get_mockups(produto, imagens)

    modelos = ModeloProduto.get_modelos_do_produto(produto)
    cores = Cor.get_cores_ativas()

    # Busca os modelos
    modelo_array = []
    for m in modelos:
        modelo_array.append(m.modelo_id)
    tamanhos_modelo = TamanhoModelo.objects.filter(
        modelo__in=modelo_array).exclude(ativo=False)

    # Pega o tamanho dos modelos
    tamanhos_do_modelo = []
    for tm in tamanhos_modelo:
        tamanhos_do_modelo.append(tm.tamanho.id)

    # Filtra todos os tamanhos do modelo
    tamanhos = Tamanho.get_tamanhos_ativos().filter(id__in=tamanhos_do_modelo)

    # Monta uma json de tamanhos para controlar a selecao do cliente na tela
    tamanho_modelo_dict = dict()
    for m in modelos:
        tamanho_list = []
        for tm in tamanhos_modelo:
            if tm.modelo.id == m.modelo.id:
                for ta in tamanhos:
                    if ta.id == tm.tamanho.id:
                        tamanho_list.append(ta.slug)
        tamanho_modelo_dict.update({m.modelo.descricao: tamanho_list})

    produtos_relacionados = Produto.objects.filter(
        subcategoria=produto.subcategoria)[:8]
    subcategorias = SubCategoria.get_subcategorias_ativas()

    context = {
        'produto': produto,
        'imagens': imagens,
        'mockups': mockups,
        'form': ProdutoDetalheForm(),
        'subcategorias': subcategorias,
        'cores': cores,
        'tamanhos': tamanhos,
        'tamanhos_modelo': tamanhos_modelo,
        'tamanho_modelo_dict': tamanho_modelo_dict,
        'modelos': modelos,
        'quantidade_item': get_quantidade_items_carrinho(request),
        'produtos_relacionados': produtos_relacionados
    }
    return render(request, 'catalogo/produto_detalhe.html', context)


"""  --------------- PRIVATE AREA --------------------- """


def __adicionar_item_carrinho(request, produto, modelo, cor, tamanho, quantidade):
    """ Funcao responsavel por adicionar items no carrinho """

    carrinho = Carrinho()
    modelo = int(modelo)

    if 'carrinho' in request.session:
        uuid = request.session['carrinho']
        carrinho = Carrinho.objects.get(uuid=uuid)
    else:
        carrinho.save()
        request.session['carrinho'] = str(carrinho.uuid)

    cor = Cor.objects.get(slug=cor)
    tamanho = Tamanho.objects.get(slug=tamanho)
    quantidade = int(quantidade)

    item = ItemCarrinho.objects.filter(
        produto=produto, carrinho=carrinho, cor=cor, tamanho=tamanho, modelo_produto_id=modelo)

    if item:
        ItemCarrinho.objects.filter(produto=produto, carrinho=carrinho, cor=cor, tamanho=tamanho, modelo_produto_id=modelo).update(
            quantidade=item[0].quantidade + quantidade)
    else:
        ItemCarrinho(carrinho=carrinho, produto=produto, modelo_produto_id=modelo,
                     quantidade=quantidade, tamanho=tamanho, cor=cor).save()


def __get_page_obj(request, produtos):
    """ funcao responsavel por paginacao """
    paginator = Paginator(produtos, 32)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def __get_mockups(produto, imagens):
    """ Monta todos os mockups e da um replace na imagem pra ficar com baixo consumo de banda """

    mockups = {0: produto.imagem_principal.url}

    for imagem in imagens:
        imagemPerformada = imagem.imagem.url
        mock = {imagem.id: imagemPerformada}
        mockups.update(mock)

    return mockups
