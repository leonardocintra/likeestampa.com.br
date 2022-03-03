from re import S
from django.test import TestCase, Client
from django.shortcuts import resolve_url as r
from django.urls import reverse
from catalogo.models import Cor, Modelo, ModeloProduto, Produto, ProdutoImagem, SubCategoria, Tamanho

client = Client()


class SubCategoriaListView(TestCase):
    def setUp(self):
        self.subcategoria = SubCategoria.objects.create(
            nome='Programação', slug='programacao')
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
    def setUp(self):
        subcategoria = SubCategoria.objects.create(
            nome='Programação', slug='programacao')
        self.obj = Produto.objects.create(
            nome=f'Camiseta Python Django',
            descricao='Camiseta 100 de Algodão - Malha Final etc tal',
            slug=f'camiseta-python-django',
            subcategoria=subcategoria,
            imagem_principal='/image/upload/camiseta-django',
            imagem_design='Imagem Cloudinary 2',
        )

        self.imagens = ProdutoImagem.objects.create(
            produto=self.obj,
            imagem='/image/upload/ronaldinho-gaucho',
        )

        self.tamanho = Tamanho.objects.create(nome='G', slug='g')
        self.cor = Cor.objects.create(nome='Vermelho', slug='vermelho')
        self.modelo = Modelo.objects.create(descricao='Cropped')

        self.modelo_produto = ModeloProduto.objects.create(
            produto=self.obj, modelo=self.modelo)

        self.response = self.client.get(r('catalogo:produto', self.obj.slug))

    def test_template(self):
        self.assertTemplateUsed(self.response, 'catalogo/produto_detalhe.html')

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_imagem_mockup_replace_low(self):
        # Os mockups deve ter o w_75 (width=75)
        self.assertContains(self.response, '/image/upload/q_auto:low,w_75')
    
    def test_imagem_principal_mockup_replace_low(self):
        # A imagem principal nao deve ter o w_75 (width=75)
        self.assertContains(self.response, '/image/upload/q_auto:low/v1')

    def test_html(self):
        contents = (self.obj.nome, self.obj.descricao, self.obj.subcategoria)

        with self.subTest():
            for expected in contents:
                self.assertContains(self.response, expected)

    def test_post(self):
        data = {
            'modelo': str(self.modelo_produto.pk),
            'cor': 'vermelho',
            'tamanho': 'g',
            'quantidade': 5
        }
        self.response = self.client.post(
            r('catalogo:produto', self.obj.slug), data=data)
        self.assertEqual(302, self.response.status_code)
