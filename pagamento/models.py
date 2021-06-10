from django.db import models
from localflavor.br.models import BRCPFField
from pedido.models import Pedido


class Pagamento(models.Model):
    pedido = models.ForeignKey(
        Pedido, related_name="pagamento_pedido", on_delete=models.CASCADE)
    valor_pedido = models.DecimalField(max_digits=999, decimal_places=2)
    parcelas = models.IntegerField(default=1)
    metodo_pagamento = models.CharField(max_length=250)
    email = models.EmailField()
    numero_documento = BRCPFField("CPF")
    created_at = models.DateField('Criado em', auto_now_add=True)
    updated_at = models.DateField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'pagamento'
        verbose_name_plural = 'Pagamentos'
        verbose_name = 'Pagamento'

    def __str__(self):
        return self.pedido


class PagamentoMercadoPago(models.Model):
    pagamento = models.ForeignKey(
        Pagamento, related_name="pagamento_mercado_pago", on_delete=models.CASCADE)
    mercado_pago_id = models.CharField(
        max_length=250, blank=True, db_index=True)
    mercado_pago_status = models.CharField(max_length=250, blank=True)
    mercado_pago_status_detail = models.CharField(max_length=250, blank=True)
    created_at = models.DateField('Criado em', auto_now_add=True)
    updated_at = models.DateField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'pagamento_mercado_pago'
        verbose_name_plural = 'Pagamentos do MP'
        verbose_name = 'Pagamento do MP'

    def __str__(self):
        return self.pedido
