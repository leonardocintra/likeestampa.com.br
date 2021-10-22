from django.test import TestCase
from django.shortcuts import resolve_url as r
from catalogo.models import Cor, Modelo, ModeloProduto, Produto, SubCategoria, Tamanho
from catalogo.tests.test_model import get_fake_produto


class ProdutoListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        subcategoria = SubCategoria.objects.create(
            nome='Programação', slug='programacao')
        for produto_id in range(60):
            Produto.objects.create(
                nome=f'Camiseta Python Django {produto_id}',
                descricao='Camiseta 100 de Algodão - Malha Final etc tal',
                slug=f'camiseta-python-django-{produto_id}',
                subcategoria=subcategoria,
                imagem_principal='Imagem Cloudinary 1',
                imagem_design='Imagem Cloudinary 2',
            )

    def setUp(self):
        self.response = self.client.get(r('core:index'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'index.html')

    def test_view_url_existe_rota_produto(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

    def test_is_not_paginated(self):
        self.assertTrue('is_paginated' in self.response.context)
        self.assertFalse(self.response.context['is_paginated'])

    def test_produto_mostrar_tela_inicial_false(self):
        pass  # fazer esse teste


class ProdutoDetailViewTest(TestCase):
    def setUp(self):
        subcategoria = SubCategoria.objects.create(
            nome='Programação', slug='programacao')
        self.obj = Produto.objects.create(
            nome=f'Camiseta Python Django',
            descricao='Camiseta 100 de Algodão - Malha Final etc tal',
            slug=f'camiseta-python-django',
            subcategoria=subcategoria,
            imagem_principal='Imagem Cloudinary 1',
            imagem_design='Imagem Cloudinary 2',
        )

        self.response = self.client.get(r('catalogo:produto', self.obj.slug))

    def test_template(self):
        self.assertTemplateUsed(self.response, 'catalogo/produto_detalhe.html')

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_html(self):
        contents = (self.obj.nome, self.obj.descricao, self.obj.subcategoria)

        with self.subTest():
            for expected in contents:
                self.assertContains(self.response, expected)

    def test_post(self):
        produto = Produto.objects.first()
        modelo = Modelo.objects.create(descricao='Cropped')
        modelo_produto = ModeloProduto.objects.create(produto=produto, modelo=modelo)
        Cor.objects.create(nome='Vermelho', slug='vermelho')
        Tamanho.objects.create(nome='G', slug='g')
        data = {
            'modelo': str(modelo_produto.pk),
            'cor': 'vermelho',
            'tamanho': 'g',
            'quantidade': 5
        }
        self.response = self.client.post(
            r('catalogo:produto', self.obj.slug), data=data)
        self.assertEqual(302, self.response.status_code)
