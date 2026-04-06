from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path('<int:pk>/', views.PedidoDetailView.as_view(), name='pedido'),
    path('pedido_finalizado_mercado_pago', views.pedido_finalizado_mercado_pago, name='pedido_finalizado_mercado_pago'),
]
