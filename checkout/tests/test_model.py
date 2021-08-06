import uuid
from django.test import TestCase
from checkout.models import Carrinho, ItemCarrinho
from catalogo.models import Modelo, ModeloProduto, ModeloVariacao, Produto, SubCategoria, TipoVariacao, Variacao
from catalogo.tests.test_model import create_produto

UUID_FAKE = 'f2ce90d6-422b-45d6-8345-a31d223d75d0'


class CarrinhoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Carrinho.objects.create(uuid=UUID_FAKE)

    def test_create(self):
        self.assertTrue(Carrinho.objects.exists())

    def test_str(self):
        carrinho = Carrinho.objects.get(id=1)
        self.assertEqual(UUID_FAKE, str(carrinho))


class ItemCarrinhoModelTest(TestCase):
    def setUp(self):
        Carrinho.objects.create(uuid=UUID_FAKE)
        carrinho = Carrinho.objects.get(id=1)
        produto = create_produto()

        Modelo.objects.create(descricao='T-Shirt')
        modelo_produto = ModeloProduto.objects.create(produto=produto)
        variacao_tamanho = Variacao.objects.create(descricao='Tamanho', )
        variacao_cor = Variacao.objects.create(descricao='Cor', )
        tp_tamanho = TipoVariacao.objects.create(
            descricao='P', variacao=variacao_tamanho,)
        tp_cor = TipoVariacao.objects.create(
            descricao='Azul', variacao=variacao_cor,)

        tamanho = ModeloVariacao.objects.create(
            modelo_produto=modelo_produto,
            tipo_variacao=tp_tamanho
        )
        cor = ModeloVariacao.objects.create(
            modelo_produto=modelo_produto,
            tipo_variacao=tp_cor
        )

        self.obj = ItemCarrinho.objects.create(
            carrinho=carrinho,
            produto=produto,
            cor=cor,
            tamanho=tamanho,
            modelo_produto=modelo_produto
        )

    def test_create(self):
        self.assertTrue(ItemCarrinho.objects.exists())

    def test_str(self):
        self.assertEqual('Camiseta NodeJs', str(self.obj))
