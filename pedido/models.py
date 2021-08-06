import uuid
from django.contrib.auth.models import User
from django.db import models
from catalogo.models import ModeloProduto, ModeloVariacao, Produto
from usuario.models import EnderecoCliente


GATEWAY_PAGAMENTO = (
    ('mercado_pago', 'Mercado Pago'),
    ('pagseguro_uol', 'PagSeguro UOL'),
)


class Pedido(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    endereco_cliente = models.ForeignKey(EnderecoCliente, on_delete=models.PROTECT, null=True)
    pago = models.BooleanField(default=False)
    valor_total = models.DecimalField(
        max_digits=999, decimal_places=2, default=1)
    valor_items = models.DecimalField(
        max_digits=999, decimal_places=2, default=1)
    valor_frete = models.DecimalField(
        max_digits=999, decimal_places=2, default=1)
    gateway_pagamento = models.CharField(
        choices=GATEWAY_PAGAMENTO, default='mercado_pago', max_length=20)
    frete_id = models.PositiveIntegerField(default=0)
    frete_nome = models.CharField(max_length=100, null=True)
    pedido_seller = models.CharField(max_length=100, null=True)
    request_seller = models.JSONField('Request feito no seller', null=True, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'pedido'
        verbose_name_plural = 'Pedidos'
        verbose_name = 'Pedido'



class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name='pedido_item')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    cor = models.ForeignKey(
        ModeloVariacao, on_delete=models.PROTECT, related_name='item_pedido_cor')
    tamanho = models.ForeignKey(
        ModeloVariacao, on_delete=models.PROTECT, related_name='item_pedido_tamanho')
    modelo_produto = models.ForeignKey(
        ModeloProduto, on_delete=models.PROTECT, related_name='item_pedido_modelo')
    quantidade = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'item_pedido'
        verbose_name_plural = 'Itens dos pedidos'
        verbose_name = 'Item do pedido'

    def __str__(self):
        return self.produto.nome
