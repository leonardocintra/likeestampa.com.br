from django.conf import settings
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from checkout.views import get_quantidade_items_carrinho
from checkout.models import Carrinho, ItemCarrinho
from .forms import ProdutoDetalheForm
from .models import Cor, Produto, ProdutoImagem, SubCategoria, ModeloProduto, Tamanho, TamanhoModelo


class SubCategoriaListView(ListView):
    template_name = 'catalogo/list_by_categoria.html'
    paginate_by = 32
    model = Produto

    def get_queryset(self):
        queryset = Produto.objects.filter(
            subcategoria__slug=self.kwargs['slug']).exclude(ativo=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(SubCategoriaListView, self).get_context_data(**kwargs)
        context['subcategorias'] = SubCategoria.objects.all().exclude(ativo=False)
        context['sub_categoria_selecionada'] = get_object_or_404(
            SubCategoria, slug=self.kwargs['slug'])
        return context


def produto(request, slug):
    """ Pagina de detalhes do produto """
    produto = Produto.objects.get(slug=slug)

    if request.method == 'POST':
        form = ProdutoDetalheForm(request.POST)
        adicionar_item_carrinho(request, produto, form.data['modelo'],
                                form.data['cor'], form.data['tamanho'], form.data['quantidade'])
        return redirect(reverse("checkout:carrinho"))

    imagens = ProdutoImagem.objects.filter(produto=produto)
    # Adiciona no mockup a imagem principal (pelo menos a imagem 0)

    mockups = {0: produto.imagem_principal.url}

    url_cloudinary = "https://res.cloudinary.com/like-estampa"
    if settings.DEBUG:
        url_cloudinary = "http://res.cloudinary.com/leonardocintra"

    for imagem in imagens:
        imagemPerformada = imagem.imagem.url.replace(
            "{0}/image/upload".format(url_cloudinary), "{0}/image/upload/q_auto:low".format(url_cloudinary))
        mock = {imagem.id: imagemPerformada}
        mockups.update(mock)

    # TODO: Cachear essas variaveis
    modelos = ModeloProduto.objects.filter(produto=produto)
    cores = Cor.objects.all().exclude(ativo=False)

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
    tamanhos = Tamanho.objects.all().filter(
        id__in=tamanhos_do_modelo).exclude(ativo=False)

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
    subcategorias = SubCategoria.objects.all().exclude(ativo=False)

    form = ProdutoDetalheForm(initial={
        'quantidade': '1'
    })
    context = {
        'produto': produto,
        'imagens': imagens,
        'mockups': mockups,
        'form': form,
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


def adicionar_item_carrinho(request, produto, modelo, cor, tamanho, quantidade):
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


lista_por_subcategoria = SubCategoriaListView
