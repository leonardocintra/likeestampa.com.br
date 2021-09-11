from django.test import TestCase
from checkout.models import Carrinho, ItemCarrinho
from catalogo.models import Cor, Modelo, ModeloProduto, Tamanho
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

    tamanho = Tamanho.objects.create(nome='GG', )
    cor = Cor.objects.create(nome='Laranja', )

    return ItemCarrinho.objects.create(
        carrinho=carrinho,
        produto=produto,
        cor=cor,
        tamanho=tamanho,
        modelo_produto=modelo_produto
    )
