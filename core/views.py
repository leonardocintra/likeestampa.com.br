from django.views.generic.list import ListView
from catalogo.models import Produto, SubCategoria

class ProdutosListView(ListView):
    model = Produto
    paginate_by = 100
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategorias'] = SubCategoria.objects.all() 
        return context

index = ProdutosListView