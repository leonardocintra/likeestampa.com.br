from cloudinary.models import CloudinaryField
from django.core.cache import cache
from django.db import models
from core.constants import CACHE_PRODUTOS_TELA_INICIAL, CACHE_TIPOS_PRODUTOS

from seller.models import Seller


GENERO = (
    ('I', 'Infantil'),
    ('B', 'Bebê / Body'),
    ('M', 'Masculino'),
    ('F', 'Feminino'),
)


class TipoProduto(models.Model):
    """ Ex: camiseta, caneca, bones """
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField('Identificador', max_length=100, unique=True)
    ativo = models.BooleanField(default=True)
    icone_fontawesome = models.CharField(max_length=50, null=True)
    descricao = models.TextField(default='Descrição não informada')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'tipo_produto'
        verbose_name = 'Tipo produto'
        ordering = ('-created_at',)

    def __str__(self):
        return self.nome

    @classmethod
    def get_tipos_produto_ativo(cls):
        tipos_produto = cache.get(CACHE_TIPOS_PRODUTOS)
        if tipos_produto is not None:
            return tipos_produto
        tipos_produto = cls.objects.all().exclude(ativo=False)
        cache.set(CACHE_TIPOS_PRODUTOS, tipos_produto)
        return tipos_produto


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

    @classmethod
    def get_subcategorias_ativas(cls):
        subcategorias = cache.get('subcategorias')
        if subcategorias is not None:
            return subcategorias

        subcategorias = cls.objects.all().exclude(ativo=False)
        cache.set('subcategorias', subcategorias)
        return subcategorias


class Produto(models.Model):
    """Ex: camiseta sao paulo, camiseta python, moleton flutter etc"""
    nome = models.CharField(max_length=100)
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT, null=True)
    descricao = models.TextField('Descrição', blank=True)
    slug = models.SlugField('Identificador', max_length=100, unique=True)
    ativo = models.BooleanField(default=False)
    mostrar_tela_inicial = models.BooleanField(default=True)
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
        ordering = ('-created_at',)

    def __str__(self):
        return self.nome

    @classmethod
    def get_produto_by_slug(cls, slug):
        produto = cache.get(slug)
        if produto is None:
            produto = cls.objects.get(slug=slug)
            cache.set(slug, produto)
        return produto

    @classmethod
    def get_produtos_ativos(cls):
        produtos = cache.get('produtos')
        if produtos is None:
            produtos = cls.objects.all().exclude(ativo=False)
            cache.set('produtos', produtos)
        return produtos

    @classmethod
    def get_produtos_ativos_e_tela_inicial_true(cls):
        produtos = cache.get(CACHE_PRODUTOS_TELA_INICIAL)
        if produtos is None or len(produtos) < 1:
            produtos = cls.objects.all().exclude(
                ativo=False).exclude(mostrar_tela_inicial=False)
            cache.set(CACHE_PRODUTOS_TELA_INICIAL, produtos)
        return produtos


class ProdutoTipoProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo_produto = models.ForeignKey(TipoProduto, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'produto_tipo_produto'
        ordering = ('created_at',)

    def __str__(self):
        return self.tipo_produto.nome + ' - ' + self.produto.nome


class Modelo(models.Model):
    "Modelo seria: T-Shirt, mangalonga, etc"
    descricao = models.CharField(max_length=50, default='T-Shirt')
    descricao_cliente = models.CharField(max_length=50, null=True, blank=True)
    valor = models.DecimalField(
        'Valor', decimal_places=2, max_digits=999, default=51.90)
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
    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, related_name='modelo_produto')
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

    @classmethod
    def get_modelos_do_produto(cls, produto):
        cache_name = 'modelo-produto-{0}'.format(produto.slug)
        modelos_produto = cache.get(cache_name)
        if modelos_produto is None:
            modelos_produto = cls.objects.filter(produto=produto)
            cache.set(cache_name, modelos_produto)
        return modelos_produto


class Cor(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    valor = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=60, unique=True)
    ativo = models.BooleanField(default=True)
    order_exibicao = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'cor'
        verbose_name_plural = 'Cores'
        verbose_name = 'Cor'
        ordering = ('order_exibicao',)

    def __str__(self):
        return self.nome

    @classmethod
    def get_cores_ativas(cls):
        cores = cache.get('cores')
        if cores is None:
            cores = cls.objects.all().exclude(ativo=False)
            cache.set('cores', cores)
        return cores


class Tamanho(models.Model):
    nome = models.CharField(max_length=10, unique=True)
    slug = models.SlugField(max_length=15, unique=True)
    ativo = models.BooleanField(default=True)
    order_exibicao = models.PositiveIntegerField(default=0)
    descricao_cliente = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'tamanho'
        verbose_name_plural = 'Tamanhos'
        verbose_name = 'tamanho'
        ordering = ('order_exibicao',)

    def __str__(self):
        return self.nome

    @classmethod
    def get_tamanhos_ativos(cls):
        tamanhos = cache.get('tamanhos')
        if tamanhos is None:
            tamanhos = cls.objects.all().exclude(ativo=False)
            cache.set('tamanhos', tamanhos)
        return tamanhos


class TamanhoModelo(models.Model):
    """ 
        O tamanho P M G GG por exemplo nao se aplica a canecas e roupas infantis
        Nesse caso aqui serve para amarrar o tamnho de acordo com o modelo vendido
        Modelos podem ser caneca, camiseta, avental sacou ?
    """
    tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'tamanho_modelo'
        verbose_name_plural = 'Tamanhos e Modelos'
        verbose_name = 'Tamanhos e Modelos'
        ordering = ('created_at', )

    def __str__(self):
        return self.tamanho.nome + ' - ' + self.modelo.descricao


class CorModelo(models.Model):
    """
        As cores são diferentes para todos os tipos de modelos.
        Por enquanto, usamos apenas o seller dimona
        Basear nesse catalogo: https://res.cloudinary.com/dimona/image/upload/v1644522960/Dropsimples/Cata%CC%81logo_Drop_2022_Sem_Polo.pdf
    """
    cor = models.ForeignKey(Cor, on_delete=models.CASCADE)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'cor_modelo'
        verbose_name_plural = 'Cores e Modelos'
        verbose_name = 'Cor e Modelos'
        ordering = ('created_at', )

    def __str__(self):
        return self.modelo.descricao + ' - ' + self.cor.nome


class ProdutoImagem(models.Model):
    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, related_name='produto_imagem')
    imagem = CloudinaryField('Mockup')
    order_exibicao = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'produto_imagem'
        verbose_name_plural = 'Imagens'
        verbose_name = 'Produto Imagem'
        ordering = ('order_exibicao',)

    def __str__(self):
        return self.produto.nome


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
