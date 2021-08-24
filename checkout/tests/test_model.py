import uuid
from django.test import TestCase
from checkout.models import Carrinho, ItemCarrinho
from catalogo.models import Modelo, ModeloProduto, ModeloVariacao, Produto, SubCategoria, TipoVariacao, Variacao
from catalogo.tests.test_model import get_fake_produto

UUID_FAKE_CARRINHO = 'f2ce90d6-422b-45d6-8345-a31d223d75d0'


class CarrinhoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Carrinho.objects.create(uuid=UUID_FAKE_CARRINHO)

    def test_create(self):
        self.assertTrue(Carrinho.objects.exists())

    def test_str(self):
        carrinho = Carrinho.objects.get(id=1)
        self.assertEqual(UUID_FAKE_CARRINHO, str(carrinho))


class ItemCarrinhoModelTest(TestCase):
    def setUp(self):
        self.obj = get_fake_carrinho_com_items()

    def test_create(self):
        self.assertTrue(ItemCarrinho.objects.exists())

    def test_str(self):
        self.assertEqual('Camiseta NodeJs', str(self.obj))


def get_fake_carrinho_com_items():
    carrinho = Carrinho.objects.create(uuid=UUID_FAKE_CARRINHO)
    produto = get_fake_produto()

    modelo = Modelo.objects.create(descricao='T-Shirt')
    modelo_produto = ModeloProduto.objects.create(
        produto=produto, modelo=modelo)
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

    return ItemCarrinho.objects.create(
        carrinho=carrinho,
        produto=produto,
        cor=cor,
        tamanho=tamanho,
        modelo_produto=modelo_produto
    )
