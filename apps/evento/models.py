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
    evento_atual = models.BooleanField(default=False)
    origem = models.SlugField(max_length=100, default='likeestampa')
    data_ocorrencia = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'evento_pedido'
        verbose_name_plural = 'Evento dos pedidos'
        verbose_name = 'Evento do pedido'


def criar_evento(evento_id, pedido):
    # TODO: status pode ir para um redis
    evento_existe = EventoPedido.objects.filter(pedido=pedido, evento_id=evento_id)
    if not evento_existe:
        status = Status.objects.get(pk=evento_id)
        EventoPedido.objects.create(evento=status, pedido=pedido)
