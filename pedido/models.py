from django.db import models
from localflavor.br.models import BRCPFField
import uuid


class Pedido(models.Model):
    cpf = BRCPFField("CPF")
    peoplesoft_pessoa_id = models.IntegerField(null=False)
    peoplesoft_endereco_id = models.IntegerField(null=False)
    pago = models.BooleanField(default=False)
    created_at = models.DateField('Criado em', auto_now_add=True)
    updated_at = models.DateField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'pedido'
        verbose_name_plural = 'Pedidos'
        verbose_name = 'Pedido'

    def __str__(self):
        return self.cpf