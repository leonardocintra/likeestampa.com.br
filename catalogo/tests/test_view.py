from django.test import TestCase
from django.shortcuts import resolve_url as r
from catalogo.models import Produto, SubCategoria


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

        self.resp = self.client.get(r('catalogo:produto', self.obj.slug))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)
