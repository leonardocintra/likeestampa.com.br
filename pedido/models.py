from django.db import models
from localflavor.br.models import BRCPFField
import uuid

GATEWAY_PAGAMENTO = (
    ('mercado_pago', 'Mercado Pago'),
    ('pagseguro_uol', 'PagSeguro UOL'),
)


class Pedido(models.Model):
    cpf = BRCPFField("CPF")
    peoplesoft_pessoa_id = models.IntegerField(null=False)
    peoplesoft_endereco_id = models.IntegerField(null=False)
    pago = models.BooleanField(default=False)
    gateway_pagamento = models.CharField(choices=GATEWAY_PAGAMENTO, default='mercado_pago', max_length=20)
    created_at = models.DateField('Criado em', auto_now_add=True)
    updated_at = models.DateField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'pedido'
        verbose_name_plural = 'Pedidos'
        verbose_name = 'Pedido'

    def __str__(self):
        return self.cpf
