from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from checkout.views import get_quantidade_items_carrinho
from checkout.models import Carrinho, Item
from .forms import ProdutoDetalheForm
from .models import Produto, SubCategoria, ProdutoImagem, ProdutoVariacao


class ProdutosListView(ListView):
    paginate_by = 100
    template_name = 'index.html'

    def get_queryset(self):
        queryset = Produto.objects.exclude(ativo=False)
        q = self.request.GET.get('q', '')
        if q:
            queryset = queryset.filter(nome__icontains=q).exclude(ativo=False)

        queryset = _busca_genero(self, queryset)

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
            subcategoria__slug=self.kwargs['slug'])

        queryset = _busca_genero(self, queryset)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(SubCategoriaListView, self).get_context_data(**kwargs)
        context['subcategorias'] = SubCategoria.objects.all().exclude(ativo=False)
        context['produto_imagens'] = ProdutoImagem.objects.all()
        context['sub_categoria_selecionada'] = get_object_or_404(
            SubCategoria, slug=self.kwargs['slug'])
        return context


def produto(request, slug):
    """ Pagina de detalhes do produto """
    produto = Produto.objects.get(slug=slug)
    variacoes = ProdutoVariacao.objects.filter(produto=produto)
    
    if request.method == 'POST':
        form = ProdutoDetalheForm(request.POST)
        adicionar_item_carrinho(request, produto, variacoes, form.data['cor'], form.data['tamanho'], form.data['quantidade'])
        return redirect(reverse("checkout:carrinho"))
    
    produtos_relacionados = Produto.objects.filter(
        subcategoria=produto.subcategoria)[:4]
    subcategorias = SubCategoria.objects.all().exclude(ativo=False)


    form = ProdutoDetalheForm(initial={
        'quantidade': '1'
    })
    context = {
        'produto': produto,
        'form': form,
        'subcategorias': subcategorias,
        'variacoes': variacoes,
        'quantidade_item': get_quantidade_items_carrinho(request),
        'produtos_relacionados': produtos_relacionados
    }
    return render(request, 'catalogo/produto_detalhe.html', context)


def adicionar_item_carrinho(request, produto, variacoes, cor, tamanho, quantidade):
    carrinho = Carrinho()

    if 'carrinho' in request.session:
        uuid = request.session['carrinho']
        carrinho = Carrinho.objects.get(uuid=uuid)
    else:
        carrinho.save()
        request.session['carrinho'] = str(carrinho.uuid)

    cor = variacoes.get(tipo_variacao_id=int(cor))
    tamanho = variacoes.get(tipo_variacao_id=int(tamanho))
    quantidade = int(quantidade)

    item = Item.objects.filter(
        produto=produto, carrinho=carrinho, cor=cor, tamanho=tamanho)

    if item:
        Item.objects.filter(produto=produto, carrinho=carrinho, cor=cor, tamanho=tamanho).update(
            quantidade=item[0].quantidade + quantidade)
    else:
        Item(carrinho=carrinho, produto=produto, quantidade=quantidade, tamanho=tamanho, cor=cor).save()
    


def produto_masculino(request):
    request.session['genero'] = 'M'
    return HttpResponseRedirect('/')


def produto_feminino(request):
    request.session['genero'] = 'F'
    return HttpResponseRedirect('/')


def todos_os_produtos(request):
    request.session['genero'] = None
    return HttpResponseRedirect('/')


def _busca_genero(self, queryset):
    if 'genero' in self.request.session:
        genero = self.request.session['genero']
        if genero:
            if genero == 'F':
                queryset = queryset.exclude(genero='M')
            elif genero == 'M':
                queryset = queryset.exclude(genero='F')
            else:
                queryset = queryset
    return queryset


product_list = ProdutosListView
lista_por_subcategoria = SubCategoriaListView
