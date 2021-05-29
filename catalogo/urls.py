
from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('produto/', views.product_list.as_view(), name='product_list'),
    path('produto/<slug:slug>/', views.produto, name='produto'),
    path('categoria/<slug:slug>/', views.lista_por_subcategoria.as_view(), name='lista_por_subcategoria'),
    path('produto_masculino/', views.produto_masculino, name='produto_masculino'),
    path('produto_feminino/', views.produto_feminino, name='produto_feminino'),
]