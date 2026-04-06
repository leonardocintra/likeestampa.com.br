from django.db import models
from apps.core.constants import TIPO_FRETE, TXT_CRIADO_EM, TXT_MODIFICADO_EM


class Seller(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    site = models.CharField(max_length=100, unique=True)
    nome_contato = models.CharField(max_length=100, null=True, blank=True)
    telefone_contato = models.CharField(max_length=12, default='')
    cep = models.CharField(max_length=8)
    endereco = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)
    complemento = models.CharField(max_length=100, null=True, blank=True)
    referencia = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    frete_tipo = models.CharField(max_length=50, null=True, blank=True, choices=TIPO_FRETE)
    frete_url = models.CharField(max_length=200, null=True, blank=True)
    frete_token = models.TextField(null=True, blank=True)
    observacao = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(TXT_CRIADO_EM, auto_now_add=True)
    updated_at = models.DateTimeField(TXT_MODIFICADO_EM, auto_now=True)

    class Meta:
        db_table = 'seller'
        verbose_name_plural = 'Seller'
        verbose_name = 'Seller'
        ordering = ('nome',)

    def __str__(self):
        return self.nome


