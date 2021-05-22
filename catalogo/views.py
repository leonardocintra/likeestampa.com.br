from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, render
from .models import Produto, SubCategoria, ProdutoImagem
from services.dimona.api import get_frete


class ProdutosListView(ListView):
    paginate_by = 100
    template_name = 'index.html'

    def get_queryset(self):
        queryset = Produto.objects.all()
        q = self.request.GET.get('q', '')
        if q:
            queryset = Produto.objects.filter(nome__icontains=q)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategorias'] = SubCategoria.objects.all()
        _frete(self)
        context['frete'] = self.request.session['frete']
        return context


class SubCategoriaListView(ListView):
    template_name = 'catalogo/list_by_categoria.html'
    paginate_by = 100
    model = Produto

    def get_queryset(self):
        return Produto.objects.filter(subcategoria__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(SubCategoriaListView, self).get_context_data(**kwargs)
        context['subcategorias'] = SubCategoria.objects.all()
        context['produto_imagens'] = ProdutoImagem.objects.all()
        _frete(self)
        context['frete'] = self.request.session['frete']
        context['sub_categoria_selecionada'] = get_object_or_404(
            SubCategoria, slug=self.kwargs['slug'])
        return context


def produto(request, slug):
    """ Pagina de detalhes do produto """
    produto = Produto.objects.get(slug=slug)
    context = {
        'produto': produto
    }
    return render(request, 'catalogo/produto_detalhe.html', context)


def _frete(self):
    if self.request.GET.get('frete'):
        frete = self.request.GET.get('frete')
        frete = frete.replace('-', '').replace(' ', '')
        if len(frete) == 8 and frete.isnumeric():
            self.request.session['frete'] = get_frete(frete)


product_list = ProdutosListView
lista_por_subcategoria = SubCategoriaListView
