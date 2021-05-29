from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, render
from .models import Produto, SubCategoria, ProdutoImagem
from services.dimona.api import get_frete
from django.urls import reverse
from django.http import HttpResponseRedirect


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
        _frete(self)
        context['frete'] = self.request.session['frete']
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
        _frete(self)
        context['frete'] = self.request.session['frete']
        context['sub_categoria_selecionada'] = get_object_or_404(
            SubCategoria, slug=self.kwargs['slug'])
        return context


def produto(request, slug):
    """ Pagina de detalhes do produto """
    produto = Produto.objects.get(slug=slug)
    subcategorias = SubCategoria.objects.all().exclude(ativo=False)
    context = {
        'produto': produto,
        'subcategorias': subcategorias
    }
    return render(request, 'catalogo/produto_detalhe.html', context)


def produto_masculino(request):
    request.session['genero'] = 'M'
    return HttpResponseRedirect('/')


def produto_feminino(request):
    request.session['genero'] = 'F'
    return HttpResponseRedirect('/')


def _frete(self):
    if self.request.GET.get('frete'):
        frete = self.request.GET.get('frete')
        frete = frete.replace('-', '').replace(' ', '')
        if len(frete) == 8 and frete.isnumeric():
            self.request.session['frete'] = get_frete(frete)
    else:
        self.request.session['frete'] = None


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
