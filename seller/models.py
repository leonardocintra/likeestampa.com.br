from django.db import models


class Seller(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    site = models.CharField(max_length=100, unique=True)
    nome_contato = models.CharField(max_length=100, default='Marcelo Ostia')
    telefone_contato = models.CharField(max_length=12, default='')
    cep = models.CharField(max_length=8)
    endereco = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    complemento = models.CharField(max_length=100, null=True, blank=True)
    referencia = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    observacao = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'seller'
        verbose_name_plural = 'Seller'
        verbose_name = 'Seller'
        ordering = ('nome',)

    def __str__(self):
        return self.nome
