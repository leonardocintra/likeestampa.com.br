from datetime import datetime
from django.shortcuts import resolve_url as r
from django.test import TestCase
from catalogo.models import Categoria, ModeloProduto, Produto, SubCategoria, TipoVariacao, Variacao, ModeloVariacao
from django.db import IntegrityError


class CategoriaModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Categoria.objects.create(nome='Camisetas', slug='camiseta')

    def test_create(self):
        self.assertTrue(Categoria.objects.exists())

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


class VariacaoModelTest(TestCase):
    def setUp(self):
        self.obj = Variacao(
            descricao='Tamanho'
        )
        self.obj.save()

    def test_ativo_default_true(self):
        self.assertTrue(self.obj.ativo)

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Tamanho', str(self.obj))


class TipoVariacaoModelTest(TestCase):
    def setUp(self):
        variacao = Variacao.objects.create(descricao='Tamanho', )
        self.obj = TipoVariacao(
            descricao='P',
            variacao=variacao,
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(TipoVariacao.objects.exists())

    def test_ativo_default_true(self):
        self.assertTrue(self.obj.ativo)

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('P', str(self.obj))


class ProdutoModelTest(TestCase):
    def setUp(self):
        subcategoria = SubCategoria.objects.create(
            nome='Programação', slug='programacao', )
        self.obj = Produto(
            nome='Camiseta NodeJs',
            descricao='Camiseta feita de algodão 100% 30.1',
            slug='camiseta-nodejs',
            subcategoria=subcategoria,
            imagem_principal='Imagem do cloudinary',
            imagem_design='Imagem do cloudinary',
        )
        self.obj.save()

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


class ModeloProdutoModelTest(TestCase):
    def setUp(self):
        subcategoria = SubCategoria.objects.create(
            nome='Programação', slug='programacao', )
        produto = Produto.objects.create(
            nome='Camiseta NodeJs',
            descricao='Camiseta feita de algodão 100% 30.1',
            slug='camiseta-nodejs',
            subcategoria=subcategoria,
            imagem_principal='Imagem do cloudinary',
            imagem_design='Imagem do cloudinary',
        )
        self.obj = ModeloProduto(
            produto=produto,
            nome='Tradicional'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(ModeloProduto.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Tradicional', str(self.obj))


class ModeloVariacaoModelTest(TestCase):
    def setUp(self):
        subcategoria = SubCategoria.objects.create(
            nome='Programação', slug='programacao', )
        produto = Produto.objects.create(
            nome='Camiseta NodeJs',
            descricao='Camiseta feita de algodão 100% 30.1',
            slug='camiseta-nodejs',
            subcategoria=subcategoria,
            imagem_principal='Imagem do cloudinary',
            imagem_design='Imagem do cloudinary',
        )
        modelo = ModeloProduto.objects.create(
            produto=produto,
            nome='Tradicional'
        )
        variacao = Variacao.objects.create(descricao='Tamanho', )
        tipo_variacao = TipoVariacao.objects.create(
            descricao='P', variacao=variacao,)
        
        self.obj = ModeloVariacao(
            modelo=modelo,
            tipo_variacao=tipo_variacao,
            imagem='Imagem cloudinary',
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(ModeloVariacao.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Tradicional', str(self.obj))
