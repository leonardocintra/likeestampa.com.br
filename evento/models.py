from django.db import models
from pedido.models import Pedido


class Status(models.Model):
    descricao = models.CharField(max_length=100)
    visivel_cliente = models.BooleanField(default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'status'
        verbose_name_plural = 'Status'
        verbose_name = 'Status'

    def __str__(self):
        return self.descricao


class EventoPedido(models.Model):
    evento = models.ForeignKey(
        Status, on_delete=models.PROTECT, related_name='status')
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name='evento_pedido')
    origem = models.SlugField(max_length=100, default='likeestampa')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'evento_pedido'
        verbose_name_plural = 'Evento dos pedidos'
        verbose_name = 'Evento do pedido'

    def __str__(self):
        return self.pedido
