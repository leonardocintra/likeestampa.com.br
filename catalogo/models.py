from cloudinary.models import CloudinaryField
from django.db import models
from django.urls import reverse
from django.dispatch import receiver

from seller.models import Seller


GENERO = (
    ('I', 'Infantil'),
    ('B', 'Bebê / Body'),
    ('M', 'Masculino'),
    ('F', 'Feminino'),
)

class Categoria(models.Model):
    """ Ex: camiseta, caneca, bones """
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField('Identificador', max_length=100, unique=True)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'categoria'
        verbose_name_plural = 'categorias'
        verbose_name = 'categoria'
        ordering = ('-created_at',)

    def __str__(self):
        return self.nome


class SubCategoria(models.Model):
    """Ex: camiseta cantor, camiseta carros, caneca programação, etc"""
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField('Identificador', max_length=100, unique=True)
    icone_fontawesome = models.CharField(max_length=100, null=True)
    ativo = models.BooleanField(default=False)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'subcategoria'
        verbose_name_plural = 'subcategorias'
        verbose_name = 'subcategoria'
        ordering = ('nome',)

    def __str__(self):
        return self.nome


class Variacao(models.Model):
    """Ex: COR, Tamanho, Tipo de camiseta, Genero """
    descricao = models.CharField('Descrição', unique=True, max_length=50)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'variacao'
        verbose_name_plural = 'Variações'
        verbose_name = 'Variação'
        ordering = ('descricao',)

    def __str__(self):
        return self.descricao


class TipoVariacao(models.Model):
    """ Ex: vermelho, verde, branco | P M G GG | etc """
    descricao = models.CharField('Descrição', unique=True, max_length=50)
    ativo = models.BooleanField(default=True)
    variacao = models.ForeignKey(
        Variacao, on_delete=models.CASCADE, related_name='variacao_tipo_variacao')
    preco_variacao = models.DecimalField(
        'Preço', decimal_places=2, max_digits=999, default=51.90)
    valor_adicional = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'tipo_variacao'
        verbose_name_plural = 'Tipos Variações'
        verbose_name = 'Tipo Variação'
        ordering = ('descricao',)

    def __str__(self):
        return self.descricao


class Produto(models.Model):
    """Ex: camieta sao paulo, camiseta python, etc"""
    nome = models.CharField(max_length=100, unique=True)
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT, null=True)
    descricao = models.TextField('Descrição', blank=True)
    slug = models.SlugField('Identificador', max_length=100, unique=True)
    ativo = models.BooleanField(default=False)
    preco_base = models.DecimalField(
        'Preço base', decimal_places=2, max_digits=999, default=51.90)
    subcategoria = models.ForeignKey(
        SubCategoria, on_delete=models.CASCADE, related_name='produto_subcategoria')
    imagem_principal = CloudinaryField(
        'Imagem principal', default='NAO_INFORMADO')
    imagem_design = CloudinaryField('Imagem design', default='NAO_INFORMADO')
    genero = models.CharField(max_length=1, choices=GENERO, default='M')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'produto'
        verbose_name_plural = 'produtos'
        verbose_name = 'produto'
        ordering = ('nome',)

    def __str__(self):
        return self.nome


class Modelo(models.Model):
    "Modelo seria: T-Shirt, mangalonga, etc"
    descricao = models.CharField(max_length=50, default='T-Shirt')
    descricao_cliente = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'modelo'
        verbose_name_plural = 'Modelos'
        verbose_name = 'Modelos'
        ordering = ('descricao',)

    def __str__(self):
        return self.descricao


class ModeloProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='modelo_produto')
    modelo = models.ForeignKey(Modelo, on_delete=models.PROTECT, default=1)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'modelo_produto'
        verbose_name_plural = 'Modelos'
        verbose_name = 'Modelos'
        ordering = ('-created_at',)

    def __str__(self):
        return self.modelo.descricao


class ModeloVariacao(models.Model):
    modelo_produto = models.ForeignKey(
        ModeloProduto, on_delete=models.CASCADE, related_name='variacao_modelo_produto', null=True)
    tipo_variacao = models.ForeignKey(
        TipoVariacao, on_delete=models.PROTECT, related_name='tipo_variacao_produto', default=1)
    imagem = CloudinaryField('Imagem Variação', blank=True, null=True)
    outras_informacoes = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'modelo_variacao'
        verbose_name_plural = 'Variações do modelo'
        verbose_name = 'Variação do modelo'
        ordering = ('created_at',)

    def __str__(self):
        return self.modelo_produto.modelo.descricao


class SkuDimona(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=50)
    estilo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    cor = models.CharField(max_length=50)
    tamanho = models.CharField(max_length=50)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'sku_dimona'
        verbose_name_plural = 'SKU Dimona'
        verbose_name = 'SKUs Dimona'
        ordering = ('created_at',)

    def __str__(self):
        return self.nome
