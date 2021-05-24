from django.db import models
from django.urls import reverse
from cloudinary.models import CloudinaryField


class Categoria(models.Model):
    """ Ex: camiseta, caneca, bones """
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField('Identificador', max_length=100, unique=True)
    ativo = models.BooleanField(default=True)
    created_at = models.DateField('Criado em', auto_now_add=True)
    updated_at = models.DateField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'categoria'
        verbose_name_plural = 'categorias'
        verbose_name = 'categoria'
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse('catalogo:categoria', kwargs={'slug': self.slug})

    def __str__(self):
        return self.nome


class SubCategoria(models.Model):
    """Ex: camiseta cantor, camiseta carros, caneca programação, etc"""
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField('Identificador', max_length=100, unique=True)
    icone_fontawesome = models.CharField(max_length=100, null=True)
    ativo = models.BooleanField(default=False)
    created_at = models.DateField('Criado em', auto_now_add=True)
    updated_at = models.DateField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'subcategoria'
        verbose_name_plural = 'subcategorias'
        verbose_name = 'subcategoria'
        ordering = ('nome',)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    """Ex: camieta sao paulo, camiseta python, etc"""
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField('Descrição', blank=True)
    slug = models.SlugField('Identificador', max_length=100, unique=True)
    ativo = models.BooleanField(default=False)
    preco_base = models.DecimalField('Preço base', decimal_places=2, max_digits=999, default=0)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE)
    imagem_principal = CloudinaryField('Imagem principal', blank=True, null=True)
    created_at = models.DateField('Criado em', auto_now_add=True)
    updated_at = models.DateField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'produto'
        verbose_name_plural = 'produtos'
        verbose_name = 'produto'
        ordering = ('-created_at',)

    def __str__(self):
        return self.nome


class ProdutoImagem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='images')
    descricao = models.CharField("Descricao", max_length=200)
    imagem = CloudinaryField('image', blank=False, null=False)
    created_at = models.DateField('Criado em', auto_now_add=True)
    updated_at = models.DateField('Modificado em', auto_now=True)
    
    class Meta:
        db_table = 'produto_imagem'
        verbose_name_plural = 'produto_imagens'
        verbose_name = 'produto_imagem'
        ordering = ('-created_at',)

    def __str__(self):
        return self.produto.nome
