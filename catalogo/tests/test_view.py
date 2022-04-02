from django.test import TestCase, Client
from django.shortcuts import resolve_url as r
from django.urls import reverse
from catalogo.models import Produto, SubCategoria


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

    def test_somente_produtos_da_categoria(self):
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
        'fixtures/catalogo/produto_imagens.json',
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

    def test_somente_subcategorias_ativas(self):
        subCategorias = SubCategoria.objects.all()
        self.assertEqual(13, len(subCategorias))
        self.assertIsNotNone(self.response.context['subcategorias'])
        self.assertEqual(7, len(self.response.context['subcategorias']))

    def test_cores(self):
        self.assertIsNotNone(self.response.context['cores'])
        self.assertEqual(12, len(self.response.context['cores']))

    def test_modelos(self):
        self.assertIsNotNone(self.response.context['modelos'])
        self.assertEqual(3, len(self.response.context['modelos']))

    def test_tamanho_modelo_dict(self):
        self.assertIsNotNone(self.response.context['tamanho_modelo_dict'])
        self.assertEqual(3, len(self.response.context['tamanho_modelo_dict']))

    def test_tamanhos_modelo(self):
        self.assertIsNotNone(self.response.context['tamanhos_modelo'])
        self.assertEqual(17, len(self.response.context['tamanhos_modelo']))

    def test_imagens(self):
        self.assertIsNotNone(self.response.context['imagens'])
        self.assertEqual(3, len(self.response.context['imagens']))

    def test_tamanhos(self):
        self.assertIsNotNone(self.response.context['tamanhos'])
        self.assertEqual(12, len(self.response.context['tamanhos']))

    def test_produtos_relacionados(self):
        self.assertIsNotNone(self.response.context['produtos_relacionados'])
        self.assertEqual(
            1, len(self.response.context['produtos_relacionados']))

    def test_quantidade_item(self):
        self.assertIsNotNone(self.response.context['quantidade_item'])
        self.assertEqual(0, self.response.context['quantidade_item'])

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
