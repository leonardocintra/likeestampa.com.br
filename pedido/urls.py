from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path('', views.PedidoDetailView.as_view(), name='pedido'),
]
