from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from checkout.views import get_quantidade_items_carrinho
from checkout.models import Carrinho, ItemCarrinho
from .forms import ProdutoDetalheForm
from .models import Cor, Produto, ProdutoImagem, SubCategoria, ModeloProduto, Tamanho


class ProdutosListView(ListView):
    paginate_by = 30
    template_name = 'index.html'

    def get_queryset(self):
        queryset = Produto.objects.exclude(ativo=False)
        q = self.request.GET.get('q', '')
        if q:
            queryset = queryset.filter(nome__icontains=q).exclude(ativo=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subcategorias = SubCategoria.objects.all().exclude(ativo=False)
        context['subcategorias'] = subcategorias
        context['quantidade_item'] = get_quantidade_items_carrinho(
            self.request)
        return context


class SubCategoriaListView(ListView):
    template_name = 'catalogo/list_by_categoria.html'
    paginate_by = 100
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
    modelos = ModeloProduto.objects.filter(produto=produto)
    cores = Cor.objects.all().exclude(ativo=False)
    tamanhos = Tamanho.objects.all().exclude(ativo=False)

    produtos_relacionados = Produto.objects.filter(
        subcategoria=produto.subcategoria)[:4]
    subcategorias = SubCategoria.objects.all().exclude(ativo=False)

    form = ProdutoDetalheForm(initial={
        'quantidade': '1'
    })
    context = {
        'produto': produto,
        'imagens': imagens,
        'form': form,
        'subcategorias': subcategorias,
        'cores': cores,
        'tamanhos': tamanhos,
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


product_list = ProdutosListView
lista_por_subcategoria = SubCategoriaListView
