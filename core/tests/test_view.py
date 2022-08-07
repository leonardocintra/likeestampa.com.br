from django.core.cache import cache
from django.test import TestCase, Client
from django.shortcuts import resolve_url as r
from django.urls import reverse
from apps.catalogo.models import Produto, SubCategoria, TipoProduto
from core.constants import CACHE_PRODUTOS_TELA_INICIAL, CACHE_TIPOS_PRODUTOS


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
    fixtures = [
        'fixtures/catalogo/tipo_produto.json',
    ]

    def setUp(self):
        self.client = Client()
        cache.delete(CACHE_PRODUTOS_TELA_INICIAL)
        self.subcategoria = SubCategoria.objects.create(
            nome='Programação', slug='programacao', ativo=True)

    def test_get(self):
        response = self.client.get(reverse('core:index'))
        self.assertEqual(200, response.status_code)

    def test_template(self):
        response = self.client.get(reverse('core:index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_view_url_existe_rota_produto(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

    def test_frase_sem_produtos(self):
        response = self.client.get(reverse('core:index'))
        frase = 'Aguarde novidades da categoria!'
        self.assertContains(response, frase)

    def test_pagina_com_produto_sem_paginacao(self):
        create_produto('Produto 1', 'algumacoisa', self.subcategoria)
        response = self.client.get(reverse('core:index'))
        self.assertFalse('is_paginated' in response.context)
        self.assertIsNotNone(response.context['produtos'])
        self.assertEqual(1, len(response.context['produtos']))

    def test_esta_trazendo_produtos_cadastrados_na_listagem(self):
        quantidade_produtos = 50
        for produto_id in range(quantidade_produtos):
            create_produto(f'Camiseta {produto_id}',
                           f'camiseta-{produto_id}', self.subcategoria)
        response = self.client.get(reverse('core:index'))
        self.assertEqual(quantidade_produtos, len(Produto.objects.all()))
        self.assertIsNotNone(response.context['produtos'])
        cache.delete(CACHE_PRODUTOS_TELA_INICIAL)
        self.assertEqual(quantidade_produtos, len(
            response.context['produtos']))

    def test_nao_mostrar_produtos_ativo_false(self):
        create_produto('Caneca Ativa', 'caneca-a', self.subcategoria)
        create_produto('Desativada', 'caneca-d',
                       self.subcategoria, False)
        response = self.client.get(reverse('core:index'))
        self.assertEqual(1, len(response.context['produtos']))

    def test_nao_mostrar_produtos_com_parametro_pagina_incial_false(self):
        create_produto('Caneca A', 'caneca-a', self.subcategoria)
        create_produto('Caneca B', 'caneca-b', self.subcategoria, True, False)
        response = self.client.get(reverse('core:index'))
        self.assertEqual(1, len(response.context['produtos']))
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

    def test_produtos_cacheados(self):
        # deleta todos os produto e cache
        Produto.objects.all().delete()

        # cria o produto
        create_produto('Produto para cache',
                       'produto-para-cache', self.subcategoria)
        self.assertEqual(1, Produto.objects.count())
        self.assertEqual('Produto para cache', str(Produto.objects.first()))

        # busca o produto e bota no cache
        produtos_cacheados = Produto.get_produtos_ativos_e_tela_inicial_true()
        self.assertEqual(1, len(produtos_cacheados))
        self.assertEqual(str(produtos_cacheados.first()), 'Produto para cache')

        # atualiza o produto e refaz o request do cache
        Produto.objects.filter(
            slug='produto-para-cache').update(nome='Nome cache alterado')
        self.assertEqual('Nome cache alterado', str(Produto.objects.first()))
        produtos_cacheados2 = Produto.get_produtos_ativos_e_tela_inicial_true()

        # Ainda deve estar mostrando o valor cacheado e nao o valor alterado no banco
        self.assertEqual(str(produtos_cacheados2.first()),
                         'Produto para cache')
        response = self.client.get(reverse('core:index'))
        self.assertContains(response, 'Produto para cache')

        # deleta o cache para pegar valor atualizado
        cache.delete(CACHE_PRODUTOS_TELA_INICIAL)

        # Apos delete do cache deve mostrar o valor cacheado do ultimo update
        produtos_cacheados3 = Produto.get_produtos_ativos_e_tela_inicial_true()
        self.assertEqual(str(produtos_cacheados3.first()),
                         'Nome cache alterado')

        # No request na pagina deve mostrar o valor cacheado alterado
        response = self.client.get(reverse('core:index'))
        self.assertContains(response, 'Nome cache alterado')
        self.assertNotContains(response, 'Produto para cache')

    def test_frase_nossos_produtos(self):
        response = self.client.get(reverse('core:index'))
        frase = 'Nossos produtos'
        self.assertContains(response, frase)

    def test_tipos_produto(self):
        response = self.client.get(reverse('core:index'))
        self.assertIsNotNone(response.context['tipos_produto'])
        self.assertEqual(4, len(response.context['tipos_produto']))

    def test_tipos_produtos_somente_ativos(self):
        response = self.client.get(reverse('core:index'))
        self.assertEqual(4, len(response.context['tipos_produto']))
        self.assertEqual(5, TipoProduto.objects.count())

    def test_tipos_produtos_todos_desativados(self):
        objs = TipoProduto.objects.filter(ativo=True)
        for o in objs:
            TipoProduto.objects.filter(pk=o.id).update(ativo=False)
        cache.delete(CACHE_TIPOS_PRODUTOS)
        response = self.client.get(reverse('core:index'))
        self.assertEqual(0, len(response.context['tipos_produto']))
        frase = 'Nossos produtos'
        self.assertNotContains(response, frase)

    def test_tipo_produtos_com_icone_fontawesome(self):
        response = self.client.get(reverse('core:index'))
        self.assertContains(response, 'fa-solid fa-shirt')
        self.assertContains(response, 'fa-solid fa-mug-saucer')
        self.assertContains(response, 'fa-solid fa-mitten')

    def test_tipo_produtos_com_descricao_informada(self):
        response = self.client.get(reverse('core:index'))
        self.assertContains(response, 'Camiseta 100% algodão feita com amor pra voce!')

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
