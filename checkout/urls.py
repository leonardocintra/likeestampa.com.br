from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('carrinho/', views.carrinho, name='carrinho'),
    path('item/<int:id>/excluir', views.excluir_item_carrinho, name='excluir_item_carrinho'),
]
