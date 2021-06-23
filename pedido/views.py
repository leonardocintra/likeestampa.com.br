from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Pedido


class PedidoDetailView(DetailView):
    model = Pedido
    template_name = 'pedido/pedido.html'
