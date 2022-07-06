from django.core.paginator import Paginator
from django.views.decorators.http import require_GET, require_http_methods
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

import cloudinary

from checkout.views import get_quantidade_items_carrinho
from checkout.models import Carrinho, ItemCarrinho
from .forms import ProdutoDetalheForm
from .models import Cor, CorModelo, Modelo, Produto, ProdutoImagem, SubCategoria, ModeloProduto, Tamanho, TamanhoModelo, TipoProduto


@require_GET
def list_tipos_produto(request, slug):
    " Lista os produtos baseado na tipo selecionado "

    tipo_produto = TipoProduto.get_tipos_produto_ativo().filter(slug=slug)
    get_object_or_404(tipo_produto, slug=slug)
    subcategorias = SubCategoria.get_subcategorias_ativas()
    modelos = Modelo.objects.filter(tipo_produto__in=tipo_produto)
    modelo_produto = ModeloProduto.objects.filter(modelo__in=modelos)
    ids_produto = []
    for x in modelo_produto:
        ids_produto.append(x.produto.id)

    produtos = Produto.objects.filter(id__in=ids_produto)
    page_obj = __get_page_obj(request, produtos)

    request.session['tipo_produto'] = slug

    context = {
        'page_obj': page_obj,
        'subcategorias': subcategorias,
    }
    return render(request, 'catalogo/list_by_categoria.html', context)


@require_GET
def lista_por_subcategoria(request, slug):
    """ Lista os produtos baseado na categoria selecionada """

    subcategorias = SubCategoria.get_subcategorias_ativas()
    get_object_or_404(subcategorias, slug=slug)
    produtos = Produto.get_produtos_ativos().filter(
        subcategoria__slug=slug)
    page_obj = __get_page_obj(request, produtos)

    context = {
        'page_obj': page_obj,
        'subcategorias': subcategorias,
    }
    return render(request, 'catalogo/list_by_categoria.html', context)


@require_http_methods(["GET", "POST"])
def produto(request, slug):
    """ Pagina de detalhes do produto """

    produto = Produto.get_produto_by_slug(slug)

    if request.method == 'POST':
        form = ProdutoDetalheForm(request.POST)
        __adicionar_item_carrinho(request, produto, form.data['modelo'],
                                  form.data['cor'], form.data['tamanho'], form.data['quantidade'])
        return redirect(reverse("checkout:carrinho"))

    imagens = ProdutoImagem.objects.filter(produto=produto)

    imagem_principal_jpg = cloudinary.CloudinaryImage(str(produto.imagem_principal)).build_url(format='jpg')

    # Adiciona no mockup a imagem principal (pelo menos a imagem 0)
    mockups = __get_mockups(produto, imagens)

    # Busca os modelos e o tipos de produto (caneca, camiseta, avental, etc)
    modelos = ModeloProduto.get_modelos_do_produto(produto)
    dados_modelo = __montar_dados_modelo(modelos)

    modelo_array = []
    tipo_produto_array = []
    for m in modelos:
        tipo_produto_array.append(m.modelo.tipo_produto.id)
        modelo_array.append(m.modelo_id)

    tipo_produtos = TipoProduto.objects.filter(id__in=tipo_produto_array)

    """ Processo de trabalhar a cor dos modelos """
    # 1 - Pega a cor dos modelos
    cores_modelo = CorModelo.objects.filter(
        modelo__in=modelo_array).exclude(ativo=False)

    # 2 - Pega os ids da cor e joga num array
    cores_do_modelo = []
    for cm in cores_modelo:
        cores_do_modelo.append(cm.cor.id)

    # 3 - Filtra as cores baseado nos ids das cores do array
    cores = Cor.get_cores_ativas().filter(id__in=cores_do_modelo)

    """ Processo de trabalhar o tamanho dos modelos """
    # 1 - Pega o tamanho dos modelos
    tamanhos_modelo = TamanhoModelo.objects.filter(
        modelo__in=modelo_array).exclude(ativo=False)

    # 2 - Pega os ids do tamanho e joga num array
    tamanhos_do_modelo = []
    for tm in tamanhos_modelo:
        tamanhos_do_modelo.append(tm.tamanho.id)

    # 3 - Filtra os tamanhos baseado nos ids filtrados
    tamanhos = Tamanho.get_tamanhos_ativos().filter(id__in=tamanhos_do_modelo)

    # FINALMENTE Monta uma json de tamanhos e cores para controlar a selecao do cliente na tela
    tamanho_modelo_dict = dict()
    cor_modelo_dict = dict()
    modelo_e_tipo_produto_dict = dict()
    for m in modelos:
        modelo_e_tipo_produto_dict.update({m.id: m.modelo.tipo_produto.id})

        # monta json para o tamanho
        tamanho_list = []
        for tm in tamanhos_modelo:
            if tm.modelo.id == m.modelo.id:
                for ta in tamanhos:
                    if ta.id == tm.tamanho.id:
                        tamanho_list.append(ta.slug)
        tamanho_modelo_dict.update({m.modelo.descricao: tamanho_list})

        # monta o json para a cor
        cor_list = []
        for cm in cores_modelo:
            if cm.modelo.id == m.modelo.id:
                for co in cores:
                    if co.id == cm.cor.id:
                        cor_list.append(co.slug)
        cor_modelo_dict.update({m.modelo.descricao: cor_list})

    produtos_relacionados = Produto.objects.filter(
        subcategoria=produto.subcategoria)[:8]
    subcategorias = SubCategoria.get_subcategorias_ativas()

    context = {
        'imagem_principal_jpg': imagem_principal_jpg,
        'dados_modelo': dados_modelo,
        'tipo_produtos': tipo_produtos,
        'produto': produto,
        'imagens': imagens,
        'mockups': mockups,
        'form': ProdutoDetalheForm(),
        'subcategorias': subcategorias,
        'cores': cores,
        'cores_modelo': cores_modelo,
        'cor_modelo_dict': cor_modelo_dict,
        'tamanhos': tamanhos,
        'tamanhos_modelo': tamanhos_modelo,
        'tamanho_modelo_dict': tamanho_modelo_dict,
        'modelos': modelos,
        'modelo_e_tipo_produto_dict': modelo_e_tipo_produto_dict,
        'quantidade_item': get_quantidade_items_carrinho(request),
        'produtos_relacionados': produtos_relacionados
    }
    return render(request, 'catalogo/produto_detalhe.html', context)


"""  --------------- PRIVATE AREA --------------------- """


def __montar_dados_modelo(modelos):
    dados = []

    modelo_array = []
    tipo_produto_array = []
    for m in modelos:
        tipo_produto_array.append(m.modelo.tipo_produto.id)
        modelo_array.append(m.modelo_id)

    tipo_produtos = TipoProduto.objects.filter(id__in=tipo_produto_array)

    def __cores(modelo: Modelo):
        cores_modelo = CorModelo.objects.filter(
            modelo__in=modelo_array).exclude(ativo=False)
        cores_do_modelo = []
        for cm in cores_modelo:
            cores_do_modelo.append(cm.cor.id)
        cores = Cor.get_cores_ativas().filter(id__in=cores_do_modelo)

        data = []
        for cm in cores_modelo:
            if cm.modelo.id == modelo.modelo.id:
                for co in cores:
                    if co.id == cm.cor.id:
                        data.append(co.slug)
        return data
    
    def __tamanhos(modelo: Modelo):
        tamanhos_modelo = TamanhoModelo.objects.filter(
            modelo__in=modelo_array).exclude(ativo=False)
        tamanhos_do_modelo = []
        for tm in tamanhos_modelo:
            tamanhos_do_modelo.append(tm.tamanho.id)
        tamanhos = Tamanho.get_tamanhos_ativos().filter(id__in=tamanhos_do_modelo)

        data = []
        for tm in tamanhos_modelo:
            if tm.modelo.id == modelo.modelo.id:
                for ta in tamanhos:
                    if ta.id == tm.tamanho.id:
                        data.append(ta.slug)
        return data

    def __modelos(tipo_produto_id):
        data = []
        for m in modelos:
            if tipo_produto_id != m.modelo.tipo_produto.id:
                continue

            data.append(
                {
                    "id": m.modelo.id,
                    "nome": m.modelo.descricao,
                    "slug": m.modelo.slug,
                    "cores": __cores(m),
                    "preco": float(m.modelo.valor),
                    "tamanhos": __tamanhos(m),
                    "descricaoProduto": m.modelo.descricao_produto
                }
            )

        return data

    for t in tipo_produtos:
        dados.append(
            {
                "tipoProduto": t.id,
                "nome": t.nome,
                "modelos": __modelos(t.id)
            }
        )

    return dados


def __adicionar_item_carrinho(request, produto, modelo, cor, tamanho, quantidade):
    """
    Funcao responsavel por adicionar items no carrinho
    """

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
