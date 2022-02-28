from django.test import TestCase, Client
from django.shortcuts import resolve_url as r
from django.urls import reverse
from django.db.models.query import QuerySet
from catalogo.models import Produto, SubCategoria

quantidade_produtos = 50


def create_produto(nome, slug, subcategoria, ativo=True, mostrar_tela_inicial=True):
    Produto.objects.create(
        nome=nome,
        descricao='Camiseta 100 de Algodão - Malha Final etc tal',
        slug=slug,
        subcategoria=subcategoria,
        imagem_principal='Imagem Cloudinary 1',
        imagem_design='Imagem Cloudinary 2',
        ativo=ativo,
        mostrar_tela_inicial=mostrar_tela_inicial
    )


class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.subcategoria = SubCategoria.objects.create(
            nome='Programação', slug='programacao')
        self.response = self.client.get(r('core:index'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'index.html')

    def test_view_url_existe_rota_produto(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

    def test_frase_sem_produtos(self):
        response = self.client.get(reverse('core:index'))
        frase = 'Aguarde novidades da categoria!'
        self.assertContains(response, frase)

    def test_pagina_com_produto_sem_paginacao(self):
        create_produto('Produto 1', 'algumacoisa', self.subcategoria)
        self.assertFalse('is_paginated' in self.response.context)
        self.assertIsNotNone(self.response.context['produtos'])
        self.assertEqual(1, len(
            self.response.context['produtos']))

    def test_esta_trazendo_produtos_cadastrados_na_listagem(self):
        for produto_id in range(quantidade_produtos):
            create_produto(f'Camiseta {produto_id}',
                           f'camiseta-{produto_id}', self.subcategoria)
        self.assertEqual(quantidade_produtos, len(Produto.objects.all()))
        self.assertIsNotNone(self.response.context['produtos'])
        self.assertEqual(quantidade_produtos, len(
            self.response.context['produtos']))

    def test_nao_mostrar_produtos_ativo_false(self):
        create_produto('Caneca Ativa', 'caneca-a', self.subcategoria)
        create_produto('Desativada', 'caneca-d',
                       self.subcategoria, False)
        self.assertEqual(1, len(self.response.context['produtos']))

    def test_nao_mostrar_produtos_mostrar_pagina_incial_false(self):
        create_produto('Caneca A', 'caneca-a', self.subcategoria)
        create_produto('Caneca B', 'caneca-b', self.subcategoria, True, False)
        response = self.client.get(reverse('core:index'))
        self.assertEqual(1, len(self.response.context['produtos']))
        self.assertContains(response, 'Caneca A')
        self.assertNotContains(response, 'Caneca B')

    def test_botao_pesquisa(self):
        create_produto('Caneca React', 'caneca-a', self.subcategoria)
        create_produto('Caneca Django', 'caneca-b', self.subcategoria)
        create_produto('Caneca Linux', 'caneca-c', self.subcategoria)
        response = self.client.get('/?q=react')
        self.assertNotContains(response, 'Caneca Django')
        self.assertNotContains(response, 'Caneca Linux')
        self.assertContains(response, 'Caneca React')

    def test_sem_paginacao(self):
        pass

    def test_paginacao(self):
        pass


class AboutViewTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('core:about'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'about.html')

    def test_carrinho_link(self):
        expected = 'href="{}"'.format(r('checkout:carrinho'))
        self.assertContains(self.response, expected)

    def test_index_link(self):
        expected = 'href="{}"'.format(r('core:index'))
        self.assertContains(self.response, expected)


class TrocaCancelamentoViewTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('core:trocacancelamento'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'troca-e-cancelamento.html')

    def test_carrinho_link(self):
        expected = 'href="{}"'.format(r('checkout:carrinho'))
        self.assertContains(self.response, expected)

    def test_index_link(self):
        expected = 'href="{}"'.format(r('core:index'))
        self.assertContains(self.response, expected)


class TermosDeUsoViewTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('core:termos'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'termos-de-uso.html')

    def test_carrinho_link(self):
        expected = 'href="{}"'.format(r('checkout:carrinho'))
        self.assertContains(self.response, expected)

    def test_index_link(self):
        expected = 'href="{}"'.format(r('core:index'))
        self.assertContains(self.response, expected)
