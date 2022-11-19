from django.test import TestCase, Client
from django.shortcuts import resolve_url as r
from django.urls import reverse
from apps.catalogo.models import Produto, SubCategoria, TipoProduto

fixtures_geral = [
    'fixtures/seller/seller.json',
    'fixtures/catalogo/subcategoria.json',
    'fixtures/catalogo/modelo.json',
    'fixtures/catalogo/produtos.json',
    'fixtures/catalogo/modelo_produto.json',
    'fixtures/catalogo/cor.json',
    'fixtures/catalogo/cor_modelo.json',
    'fixtures/catalogo/tamanho.json',
    'fixtures/catalogo/tamanho_modelo.json',
    'fixtures/catalogo/tipo_produto.json',
    'fixtures/catalogo/produto_imagens.json',
]


class ListaPorTipoProduto(TestCase):
    fixtures = fixtures_geral

    def setUp(self) -> None:
        self.client = Client()
        self.obj = TipoProduto.objects.get(pk=2)
        self.response = self.client.get(
            reverse('catalogo:tipo_produto', kwargs={'slug': self.obj.slug}))
        self.session = self.client.session

    def test_self_obj(self):
        self.assertEqual('Canecas', str(self.obj))

    def test_template(self):
        self.assertTemplateUsed(
            self.response, 'catalogo/list_by_categoria.html')

    def test_somente_produtos_do_tipo_produto_selecionado_deve_aparecer(self):
        self.assertEqual(7, len(Produto.objects.all()))
        self.assertEqual(4, len(self.response.context['page_obj']))

    def test_tipo_produto_not_found(self):
        response = self.client.get(
            reverse('catalogo:tipo_produto', kwargs={'slug': 'nao-existe'}))
        self.assertEqual(404, response.status_code)

    def test_session(self):
        self.assertEqual('canecas', self.session['tipo_produto'])


class ListaPorSubCategoriaViewTest(TestCase):
    fixtures = fixtures_geral

    def setUp(self):
        self.subcategoria = SubCategoria.objects.get(pk=1)
        self.response = self.client.get(
            reverse('catalogo:lista_por_subcategoria', kwargs={'slug': self.subcategoria.slug}))

    def test_template(self):
        self.assertTemplateUsed(
            self.response, 'catalogo/list_by_categoria.html')

    def test_sub_categoria(self):
        subcategoria = self.response.context['subcategorias']
        self.assertIsNotNone(subcategoria)
        self.assertEqual(7, len(subcategoria))

    def test_subcategoria_inativa_nao_pode_aparecer(self):
        self.assertContains(self.response, 'Programação')
        self.assertNotContains(self.response, 'Universo / Espaço')

    def test_somente_produtos_da_categoria(self):
        self.assertEqual(7, len(Produto.objects.all()))
        self.assertEqual(2, len(self.response.context['page_obj']))

    def test_subcategoria_not_found(self):
        response = self.client.get(
            reverse('catalogo:lista_por_subcategoria', kwargs={'slug': 'nao-existe'}))
        self.assertEqual(404, response.status_code)


class ProdutoViewTest(TestCase):
    fixtures = fixtures_geral

    def setUp(self):
        self.client = Client()
        self.obj = Produto.objects.get(pk=4)
        self.response = self.client.get(r('catalogo:produto', self.obj.slug))

    def test_template(self):
        self.assertTemplateUsed(self.response, 'catalogo/produto_detalhe.html')

    def test_subcategoria_inativa_nao_pode_aparecer(self):
        self.assertContains(self.response, 'Programação')
        self.assertNotContains(self.response, 'Universo / Espaço')

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_imagem_jpg(self):
        self.assertContains(self.response, '.jpg')

    def test_somente_subcategorias_ativas(self):
        subCategorias = SubCategoria.objects.all()
        self.assertEqual(13, len(subCategorias))
        self.assertIsNotNone(self.response.context['subcategorias'])
        self.assertEqual(7, len(self.response.context['subcategorias']))

    def test_cores(self):
        self.assertIsNotNone(self.response.context['cores'])
        self.assertEqual(10, len(self.response.context['cores']))

    def test_modelos(self):
        self.assertIsNotNone(self.response.context['modelos'])
        self.assertEqual(4, len(self.response.context['modelos']))

    def test_tamanhos_modelo(self):
        self.assertIsNotNone(self.response.context['tamanhos_modelo'])
        self.assertEqual(18, len(self.response.context['tamanhos_modelo']))

    def test_imagens(self):
        self.assertIsNotNone(self.response.context['imagens'])
        self.assertEqual(3, len(self.response.context['imagens']))

    def test_tamanhos(self):
        self.assertIsNotNone(self.response.context['tamanhos'])
        self.assertEqual(13, len(self.response.context['tamanhos']))

    def test_produtos_relacionados(self):
        self.assertIsNotNone(self.response.context['produtos_relacionados'])
        self.assertEqual(
            2, len(self.response.context['produtos_relacionados']))

    def test_quantidade_item(self):
        self.assertIsNotNone(self.response.context['quantidade_item'])
        self.assertEqual(0, self.response.context['quantidade_item'])

    def test_html(self):
        contents = (self.obj.nome, self.obj.descricao, self.obj.subcategoria)

        with self.subTest():
            for expected in contents:
                self.assertContains(self.response, expected)

    def test_form_quantidade_inicia_com_um(self):
        self.assertEqual(
            1, self.response.context['form']['quantidade'].value())

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

    def test_tipo_produto(self):
        self.assertIsNotNone(self.response.context['tipo_produtos'])
        self.assertEqual(2, len(self.response.context['tipo_produtos']))

    def test_dados_modelo_context(self):
        self.assertIsNotNone(self.response.context['dados_modelo'])

    def test_dados_modelo_tipo_produto(self):
        dados = self.response.context['dados_modelo']
        self.assertIn("tipoProduto", dados[0])
        self.assertIn("nome", dados[0])
        self.assertIn("modelos", dados[0])
        self.assertEqual(2, len(dados))

    def test_dados_modelo_tamanho_nao_vazio(self):
        dados = self.response.context['dados_modelo']
        self.assertTrue(len(dados) > 0)
    
    def test_dados_modelo_tamanho_contem_objetos_necessarios(self):
        dados = self.response.context['dados_modelo']
        self.assertEqual("unico", dados[0]["modelos"][0]["tamanhos"][0]["slug"])
        self.assertEqual("Único", dados[0]["modelos"][0]["tamanhos"][0]["descricao"])

    def test_dados_modelo_cores_nao_vazio(self):
        dados = self.response.context['dados_modelo']
        self.assertTrue(len(dados) > 0)
    
    def test_dados_modelo_cores_contem_objetos_necessarios(self):
        dados = self.response.context['dados_modelo']
        self.assertEqual("branco", dados[0]["modelos"][0]["cores"][0]["slug"])
        self.assertEqual("Branco", dados[0]["modelos"][0]["cores"][0]["nome"])
        self.assertEqual("#FFFFFF", dados[0]["modelos"][0]["cores"][0]["valor"])

    def test_dados_modelo(self):
        dados = self.response.context['dados_modelo']
        self.assertIn("preco", dados[0]["modelos"][0])
        self.assertIn("cores", dados[0]["modelos"][0])
        self.assertIn("tamanhos", dados[0]["modelos"][0])
        self.assertIn("descricaoProduto", dados[0]["modelos"][0])
