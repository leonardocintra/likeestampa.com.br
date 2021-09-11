from datetime import datetime
from django.shortcuts import resolve_url as r
from django.test import TestCase
from catalogo.models import Categoria, ModeloProduto, Produto, SubCategoria, Modelo, SkuDimona, Cor, Tamanho
from django.db import IntegrityError


class TamanhoModelTest(TestCase):
    def setUp(self):
        self.obj = Tamanho(
            nome='P',
            slug='p'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Tamanho.objects.exists())

    def test_str(self):
        self.assertEqual('P', str(self.obj))


class CorModelTest(TestCase):
    def setUp(self):
        self.obj = Cor(
            nome='Verde Bandeira',
            slug='verde-bandeira'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Cor.objects.exists())

    def test_str(self):
        self.assertEqual('Verde Bandeira', str(self.obj))


class CategoriaModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Categoria.objects.create(nome='Camisetas', slug='camiseta')

    def test_create(self):
        self.assertTrue(Categoria.objects.exists())

    def test_str(self):
        categoria = Categoria.objects.get(id=1)
        self.assertEqual('Camisetas', str(categoria))

    def test_created_at(self):
        categoria = Categoria.objects.get(id=1)
        self.assertIsInstance(categoria.created_at, datetime)

    def test_slug_label(self):
        categoria = Categoria.objects.get(id=1)
        field_label = categoria._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'Identificador')

    def test_created_at_label(self):
        categoria = Categoria.objects.get(id=1)
        field_label = categoria._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'Criado em')

    def test_updated_at_label(self):
        categoria = Categoria.objects.get(id=1)
        field_label = categoria._meta.get_field('updated_at').verbose_name
        self.assertEquals(field_label, 'Modificado em')

    def test_nome_max_length(self):
        categoria = Categoria.objects.get(id=1)
        max_length = categoria._meta.get_field('nome').max_length
        self.assertEquals(max_length, 100)

    def test_slug_max_length(self):
        categoria = Categoria.objects.get(id=1)
        max_length = categoria._meta.get_field('slug').max_length
        self.assertEquals(max_length, 100)

    def test_first_name_max_length(self):
        categoria = Categoria.objects.get(id=1)
        max_length = categoria._meta.get_field('nome').max_length
        self.assertEquals(max_length, 100)

    def test_ativo_default_true(self):
        categoria = Categoria.objects.get(id=1)
        self.assertEquals(True, categoria.ativo)

    def test_categoria_slug_unique(self):
        with self.assertRaises(IntegrityError):
            Categoria.objects.create(nome='Camisetas', slug='camiseta')


class SubCategoriaModelTest(TestCase):
    def setUp(self):
        self.obj = SubCategoria(
            nome='Programação',
            slug='programacao'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(SubCategoria.objects.exists())

    def test_ativo_default_false(self):
        self.assertFalse(self.obj.ativo)

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Programação', str(self.obj))


class ProdutoModelTest(TestCase):
    def setUp(self):
        self.obj = get_fake_produto()

    def test_create(self):
        self.assertTrue(Produto.objects.exists())

    def test_ativo_default_false(self):
        self.assertFalse(self.obj.ativo)

    def test_genero(self):
        self.assertEqual('M', self.obj.genero)

    def test_preco_base(self):
        self.assertEqual(51.90, self.obj.preco_base)

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Camiseta NodeJs', str(self.obj))


class ModeloModelTest(TestCase):
    def setUp(self):
        self.obj = Modelo.objects.create(descricao='T-Shirt')

    def test_create(self):
        self.assertTrue(Modelo.objects.exists())

    def test_str(self):
        Modelo.objects.get(pk=self.obj.id)
        self.assertEqual('T-Shirt', str(self.obj))


class ModeloProdutoModelTest(TestCase):
    def setUp(self):
        modelo = Modelo.objects.create(descricao='T-Shirt')
        produto = get_fake_produto()
        self.obj = ModeloProduto(produto=produto, modelo=modelo)
        self.obj.save()

    def test_create(self):
        self.assertTrue(ModeloProduto.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('T-Shirt', str(self.obj))


class SkuDimonaModelTest(TestCase):
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
