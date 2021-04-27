from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from .models import Produto, SubCategoria


class ProdutosListView(ListView):
    model = Produto
    paginate_by = 100
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategorias'] = SubCategoria.objects.all()
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
        context['sub_categoria_selecionada'] = get_object_or_404(
            SubCategoria, slug=self.kwargs['slug'])
        return context


product_list = ProdutosListView
lista_por_subcategoria = SubCategoriaListView