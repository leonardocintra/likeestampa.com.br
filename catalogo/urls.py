
from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('categoria/<slug:slug>/', views.lista_por_subcategoria.as_view(), name='lista_por_subcategoria')
]