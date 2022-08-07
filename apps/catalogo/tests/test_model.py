from datetime import datetime
from django.core.cache import cache
from django.test import TestCase
from apps.catalogo.models import (TipoProduto, ModeloProduto, Produto, ProdutoImagem,
                             SubCategoria, Modelo, SkuDimona, Cor, Tamanho, TamanhoModelo, CorModelo)
from django.db import IntegrityError

from core.constants import CACHE_TIPOS_PRODUTOS


class TamanhoModelTest(TestCase):
    fixtures = ['fixtures/catalogo/tamanho.json', ]

    def setUp(self):
        self.obj = Tamanho.objects.get(pk=1)

    def test_create(self):
        self.assertTrue(Tamanho.objects.exists())

    def test_str(self):
        self.assertEqual('P', str(self.obj))


class CorModelTest(TestCase):
    fixtures = ['fixtures/catalogo/cor.json', ]

    def setUp(self):
        cache.delete('cores')
        self.obj = Cor.objects.get(pk=11)

    def test_create(self):
        self.assertTrue(Cor.objects.exists())

    def test_str(self):
        self.assertEqual('Verde Bandeira', str(self.obj))

    def test_get_cores_ativas(self):
        Cor.objects.create(nome='Cor inativa', valor='#444444',
                           slug='cor-inativa', ativo=False)
        self.assertEqual(13, Cor.objects.count())
        self.assertEqual(12, len(Cor.get_cores_ativas()))

    def test_get_cores_ativas_cache(self):
        Cor.objects.create(nome='Cor no CACHE',
                           valor='#555555', slug='cor-nova-1')
        self.assertEqual(13, len(Cor.get_cores_ativas()))
        Cor.objects.create(nome='Cor FORA do cache',
                           valor='#555556', slug='cor-nova-2')
        self.assertEqual(13, len(Cor.get_cores_ativas()))
        self.assertEqual(14, Cor.objects.count())


class CorModeloModelTest(TestCase):
    fixtures = [
        'fixtures/catalogo/tipo_produto.json',
        'fixtures/catalogo/modelo.json',
        'fixtures/catalogo/cor.json',
    ]

    def setUp(self):
        self.modelo = Modelo.objects.get(pk=1)
        self.cor = Cor.objects.get(pk=11)
        self.obj = CorModelo.objects.create(cor=self.cor, modelo=self.modelo)

    def test_create(self):
        self.assertTrue(CorModelo.objects.exists())

    def test_str(self):
        self.assertEqual('T-Shirt - Verde Bandeira', str(self.obj))

    def test_ativo_default(self):
        self.assertTrue(self.obj.ativo)


class TamanhoModeloModelTest(TestCase):
    fixtures = [
        'fixtures/catalogo/tipo_produto.json',
        'fixtures/catalogo/modelo.json',
        'fixtures/catalogo/tamanho.json',
    ]

    def setUp(self):
        self.modelo = Modelo.objects.get(pk=1)
        self.tamanho = Tamanho.objects.get(pk=1)
        self.obj = TamanhoModelo(
            tamanho=self.tamanho,
            modelo=self.modelo
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(TamanhoModelo.objects.exists())

    def test_str(self):
        self.assertEqual('P - T-Shirt', str(self.obj))

    def test_ativo_defult(self):
        self.assertTrue(self.obj.ativo)


class TipoProdutoModelTest(TestCase):
    fixtures = ['fixtures/catalogo/tipo_produto.json', ]

    def setUp(self) -> None:
        cache.delete(CACHE_TIPOS_PRODUTOS)

    def test_exists(self):
        self.assertTrue(TipoProduto.objects.exists())

    def test_str(self):
        tipo_produto = TipoProduto.objects.get(id=1)
        self.assertEqual('Camisetas', str(tipo_produto))

    def test_created_at(self):
        tipo_produto = TipoProduto.objects.get(id=1)
        self.assertIsInstance(tipo_produto.created_at, datetime)

    def test_slug_label(self):
        tipo_produto = TipoProduto.objects.get(id=1)
        field_label = tipo_produto._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'Identificador')

    def test_created_at_label(self):
        tipo_produto = TipoProduto.objects.get(id=1)
        field_label = tipo_produto._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'Criado em')

    def test_updated_at_label(self):
        tipo_produto = TipoProduto.objects.get(id=1)
        field_label = tipo_produto._meta.get_field('updated_at').verbose_name
        self.assertEquals(field_label, 'Modificado em')

    def test_nome_max_length(self):
        tipo_produto = TipoProduto.objects.get(id=1)
        max_length = tipo_produto._meta.get_field('nome').max_length
        self.assertEquals(max_length, 100)

    def test_slug_max_length(self):
        tipo_produto = TipoProduto.objects.get(id=1)
        max_length = tipo_produto._meta.get_field('slug').max_length
        self.assertEquals(max_length, 100)

    def test_first_name_max_length(self):
        tipo_produto = TipoProduto.objects.get(id=1)
        max_length = tipo_produto._meta.get_field('nome').max_length
        self.assertEquals(max_length, 100)

    def test_ativo_default_true(self):
        tipo_produto = TipoProduto.objects.get(id=1)
        self.assertEquals(True, tipo_produto.ativo)

    def test_tipo_produto_slug_unique(self):
        with self.assertRaises(IntegrityError):
            TipoProduto.objects.create(nome='Camisetas', slug='camiseta')

    def test_cache(self):
        tipo_produto = TipoProduto.get_tipos_produto_ativo()
        self.assertIsNotNone(tipo_produto)
        self.assertEqual(4, len(tipo_produto))
        TipoProduto.objects.create(nome='Teste', slug='teste')
        novo_get = TipoProduto.get_tipos_produto_ativo()
        self.assertEqual(4, len(novo_get))
        cache.delete(CACHE_TIPOS_PRODUTOS)
        novo_get2 = TipoProduto.get_tipos_produto_ativo()
        self.assertEqual(5, len(novo_get2))


class SubCategoriaModelTest(TestCase):
    fixtures = ['fixtures/catalogo/subcategoria.json', ]

    def setUp(self):
        cache.delete('subcategorias')
        self.obj = SubCategoria.objects.get(pk=1)

    def test_create(self):
        self.assertTrue(SubCategoria.objects.exists())

    def test_ativo_default_false(self):
        sub = SubCategoria.objects.create(nome='Nova cat', slug='nova-cat')
        self.assertFalse(sub.ativo)

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Programação', str(self.obj))

    def test_cache(self):
        self.assertIsNone(cache.get('subcategorias'))
        subs = SubCategoria.get_subcategorias_ativas()
        self.assertIsNotNone(cache.get('subcategorias'))
        self.assertEqual(7, len(subs))

    def test_cache_diferente_banco(self):
        subs = SubCategoria.get_subcategorias_ativas()
        self.assertEqual('Filmes', str(subs[0]))
        self.assertEqual(3, subs[0].id)
        SubCategoria.objects.filter(id=3).update(nome='Movies')
        bd = SubCategoria.objects.filter(id=3).first()
        self.assertEqual('Movies', bd.nome)  # no banco
        self.assertEqual('Filmes', str(subs[0]))   # no cache


class ProdutoModelTest(TestCase):
    fixtures = ['fixtures/seller/seller.json',
                'fixtures/catalogo/subcategoria.json',
                'fixtures/catalogo/produtos.json', ]

    def setUp(self) -> None:
        cache.delete('elixir-vertical')
        cache.delete('produtos')
        self.obj = Produto.objects.get(pk=3)
        self.subcategoria = SubCategoria.objects.get(pk=1)

    def test_create(self):
        self.assertTrue(Produto.objects.exists())

    def test_ativo_default_false(self):
        prod = Produto.objects.create(
            nome='Camiseta NodeJs',
            descricao='Camiseta feita de algodão 100% 30.1',
            slug='camiseta-nodejs',
            subcategoria=self.subcategoria,
            imagem_principal='Imagem do cloudinary',
            imagem_design='Imagem do cloudinary',
        )
        self.assertFalse(prod.ativo)

    def test_genero(self):
        self.assertEqual('M', self.obj.genero)

    def test_preco_base(self):
        self.assertEqual(51.90, float(self.obj.preco_base))

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Elixir (Vertical)', str(self.obj))

    def test_get_produto_by_slug(self):
        self.assertIsNone(cache.get('elixir-vertical'))
        produto = Produto.get_produto_by_slug('elixir-vertical')
        self.assertEqual(produto.nome, 'Elixir (Vertical)')
        self.assertIsNotNone(cache.get('elixir-vertical'))

    def test_get_produtos_ativos(self):
        Produto.objects.create(
            nome='Camiseta NodeJs',
            descricao='Camiseta feita de algodão 100% 30.1',
            slug='camiseta-nodejs',
            subcategoria=self.subcategoria,
            imagem_principal='Imagem do cloudinary',
            imagem_design='Imagem do cloudinary',
        )
        self.assertEqual(8, Produto.objects.count())
        self.assertEqual(7, len(Produto.get_produtos_ativos()))
        self.assertIsNotNone(cache.get('produtos'))


class ProdutoImagemModelTest(TestCase):
    fixtures = ['fixtures/seller/seller.json',
                'fixtures/catalogo/subcategoria.json',
                'fixtures/catalogo/produtos.json',
                'fixtures/catalogo/tipo_produto.json',
                'fixtures/catalogo/modelo.json', ]

    def setUp(self):
        self.obj = ProdutoImagem.objects.create(
            produto=Produto.objects.get(pk=2),
            imagem='imagem-cloudinary',
        )

    def test_create(self):
        self.assertTrue(ProdutoImagem.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Ronaldinho 10', str(self.obj))


class ModeloModelTest(TestCase):
    fixtures = ['fixtures/catalogo/tipo_produto.json', ]

    def setUp(self):
        self.obj = Modelo.objects.create(descricao='T-Shirt')

    def test_create(self):
        self.assertTrue(Modelo.objects.exists())

    def test_str(self):
        Modelo.objects.get(pk=self.obj.id)
        self.assertEqual('T-Shirt', str(self.obj))


class ModeloProdutoModelTest(TestCase):
    fixtures = ['fixtures/seller/seller.json',
                'fixtures/catalogo/subcategoria.json',
                'fixtures/catalogo/produtos.json',
                'fixtures/catalogo/tipo_produto.json',
                'fixtures/catalogo/modelo.json',
                'fixtures/catalogo/modelo_produto.json', ]

    def setUp(self):
        self.obj = ModeloProduto.objects.get(pk=8)

    def test_create(self):
        self.assertTrue(ModeloProduto.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('T-Shirt', str(self.obj))

    def test_get_modelos_do_produto(self):
        produto = Produto.objects.get(pk=4)
        cache.delete('modelo-produto-{0}'.format(produto.slug))
        modelos = ModeloProduto.get_modelos_do_produto(produto)
        self.assertIsNotNone(modelos)
        self.assertEqual(4, len(modelos))
        self.assertIsNotNone(
            cache.get('modelo-produto-{0}'.format(produto.slug)))


class SkuDimonaModelTest(TestCase):
    fixtures = ['fixtures/catalogo/tipo_produto.json', ]

    def setUp(self):
        modelo = Modelo.objects.create(descricao='T-Shirt')
        self.obj = SkuDimona.objects.create(
            sku='328198319',
            nome='Dimona Quality',
            estilo=modelo,
            cor='Azul',
            tamanho='G'
        )

    def test_create(self):
        self.assertTrue(SkuDimona.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Dimona Quality', str(self.obj))


def get_fake_produto():
    # DEPRECATED: usar fixtures (remover do restantes dos testes)
    subcategoria = SubCategoria.objects.create(
        nome='Programação', slug='programacao', )
    return Produto.objects.create(
        nome='Camiseta NodeJs',
        descricao='Camiseta feita de algodão 100% 30.1',
        slug='camiseta-nodejs',
        subcategoria=subcategoria,
        imagem_principal='Imagem do cloudinary',
        imagem_design='Imagem do cloudinary',
    )
