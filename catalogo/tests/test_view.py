from django.test import TestCase, Client
from django.shortcuts import resolve_url as r
from django.urls import reverse
from catalogo.models import Cor, Modelo, ModeloProduto, Produto, ProdutoImagem, SubCategoria, Tamanho, TamanhoModelo


class SubCategoriaListView(TestCase):
    fixtures = ['fixtures/catalogo/subcategoria.json']

    def setUp(self):
        self.subcategoria = SubCategoria.objects.get(pk=1)
        self.response = self.client.get(
            reverse('catalogo:lista_por_subcategoria', kwargs={'slug': 'programacao'}))

    def test_template(self):
        self.assertTemplateUsed(
            self.response, 'catalogo/list_by_categoria.html')

    def test_sub_categoria(self):
        self.assertIsNotNone(self.response.context['subcategorias'])
        self.assertIsNotNone(
            self.response.context['sub_categoria_selecionada'])

    def test_sub_categoria_not_found(self):
        pass


class ProdutoDetailViewTest(TestCase):

    fixtures = [
        'fixtures/seller/seller.json',
        'fixtures/catalogo/subcategoria.json',
        'fixtures/catalogo/modelo.json',
        'fixtures/catalogo/produtos.json',
        'fixtures/catalogo/modelo_produto.json',
        'fixtures/catalogo/cor.json',
        'fixtures/catalogo/tamanho.json',
        'fixtures/catalogo/tamanho_modelo.json',
    ]

    def setUp(self):
        self.client = Client()
        self.obj = Produto.objects.get(pk=4)
        self.response = self.client.get(r('catalogo:produto', self.obj.slug))

    def test_template(self):
        self.assertTemplateUsed(self.response, 'catalogo/produto_detalhe.html')

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_imagem_low(self):
        self.assertContains(self.response, '/image/upload/q_auto:low/v')

    def test_modelos(self):
        self.assertIsNotNone(self.response.context['modelos'])
        self.assertEqual(3, len(self.response.context['modelos']))

    def test_tamanhos(self):
        self.assertIsNotNone(self.response.context['tamanhos'])
        self.assertEqual(12, len(self.response.context['tamanhos']))

    def test_html(self):
        contents = (self.obj.nome, self.obj.descricao, self.obj.subcategoria)

        with self.subTest():
            for expected in contents:
                self.assertContains(self.response, expected)

    def test_post(self):
        data = {
            'modelo': '7',
            'cor': 'laranja',
            'tamanho': 'g',
            'quantidade': 5
        }
        self.response = self.client.post(
            r('catalogo:produto', self.obj.slug), data=data)
        self.assertEqual(302, self.response.status_code)
