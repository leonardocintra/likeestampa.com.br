
from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('<slug:slug>', views.list_tipos_produto, name='tipo_produto'),
    path('produto/<slug:slug>/', views.produto, name='produto'),
    path('categoria/<slug:slug>/', views.lista_por_subcategoria, name='lista_por_subcategoria'),
    path('catalogo/nossos-produtos/', views.produtos_dimona, name='produtos_dimona')
]
