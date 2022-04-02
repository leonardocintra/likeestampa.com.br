
from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('produto/<slug:slug>/', views.produto, name='produto'),
    path('categoria/<slug:slug>/', views.lista_por_subcategoria,
         name='lista_por_subcategoria'),
]
