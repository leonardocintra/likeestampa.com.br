from django.db import models
from django.urls import reverse


class Categoria(models.Model):
    """ Ex: camiseta, caneca, bones """
    nome = models.CharField(max_length=100)
    slug = models.SlugField('Identificador', max_length=100)
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
    nome = models.CharField(max_length=100)
    slug = models.SlugField('Identificador', max_length=100)
    icone_fontawesome = models.CharField(max_length=100, null=True)
    created_at = models.DateField('Criado em', auto_now_add=True)
    updated_at = models.DateField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'subcategoria'
        verbose_name_plural = 'subcategorias'
        verbose_name = 'subcategoria'
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse('catalogo:subcategoria', kwargs={'slug': self.slug})

    def __str__(self):
        return self.nome


class Produto(models.Model):
    """Ex: camieta sao paulo, camiseta python, etc"""
    nome = models.CharField(max_length=100)
    descricao = models.TextField('Descrição', blank=True)
    slug = models.SlugField('Identificador', max_length=100)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE)
    created_at = models.DateField('Criado em', auto_now_add=True)
    updated_at = models.DateField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'produto'
        verbose_name_plural = 'produtos'
        verbose_name = 'produto'
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse('catalogo:produto', kwargs={'slug': self.slug})

    def __str__(self):
        return self.nome
