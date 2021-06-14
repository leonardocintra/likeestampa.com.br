import uuid
from django.db import models
from catalogo.models import Produto


class Carrinho(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'carrinho'
        verbose_name_plural = 'Carrinhos'
        verbose_name = 'Carrinho'

    def __str__(self):
        return self.uuid


class Item(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)


    class Meta:
        db_table = 'item'
        verbose_name_plural = 'Itens'
        verbose_name = 'item'

    def __str__(self):
        return self.produto.nome