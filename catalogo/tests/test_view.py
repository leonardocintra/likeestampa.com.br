from django.test import TestCase
from django.shortcuts import resolve_url as r
from catalogo.models import Cor, Modelo, ModeloProduto, Produto, SubCategoria, Tamanho


class ProdutoListViewTest(TestCase):
    def setUp(self):
        self.subcategoria = SubCategoria.objects.create(
            nome='Programação', slug='programacao')
        for produto_id in range(10):
            Produto.objects.create(
                nome=f'Camiseta Python Django {produto_id}',
                descricao='Camiseta 100 de Algodão - Malha Final etc tal',
                slug=f'camiseta-python-django-{produto_id}',
                subcategoria=self.subcategoria,
                imagem_principal='Imagem Cloudinary 1',
                imagem_design='Imagem Cloudinary 2',
            )

    def test_get(self):
        response = self.client.get(r('core:index'))
        self.assertEqual(200, response.status_code)

    def test_template(self):
        response = self.client.get(r('core:index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_view_url_existe_rota_produto(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

    def test_is_not_paginated(self):
        response = self.client.get(r('core:index'))
        self.assertTrue('is_paginated' in response.context)
        self.assertFalse(response.context['is_paginated'])

    def test_esta_trazendo_produtos_cadastrados_na_listagem(self):
        response = self.client.get(r('core:index'))
        self.assertEqual(10, len(Produto.objects.all()))
        self.assertIsNotNone(response.context['produto_list'])
        # TODO: aguardando ajuda em https://pt.stackoverflow.com/questions/544047/django-testcase-n%c3%a3o-mostra-dados-no-response-context-listview
        # self.assertEqual(10, len(response.context['produto_list']))


    def test_produto_mostrar_tela_inicial_false(self):
        # Nao deve trazer produtos que esta com mostrar_tela_inicial = False
        produto = Produto.objects.create(
            nome=f'Camiseta NodeJS Express',
            descricao='Camiseta 100 de Algodão - Malha Final etc tal',
            slug=f'camiseta-nodejs-express',
            subcategoria=self.subcategoria,
            imagem_principal='Imagem Cloudinary 1',
            imagem_design='Imagem Cloudinary 2',
            mostrar_tela_inicial=False,
        )

        response = self.client.get(r('core:index'))
        self.assertFalse(produto.mostrar_tela_inicial)
        self.assertEqual(11, len(Produto.objects.all()))
        self.assertIsNotNone(response.context['produto_list'])
        # TODO: PRECISA TESTAR QUE NAO ESTA MOSTRANDO O PRODUTO QUE NAO DEVE MOSTRAR
        # self.assertEqual(len(self.response.context_data['produto_list']), 10)
        # self.assertTrue(len(self.response.context_data['produto_list']) == 10)


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
        modelo_produto = ModeloProduto.objects.create(
            produto=produto, modelo=modelo)
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
