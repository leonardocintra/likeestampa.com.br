from django.test import TestCase
from usuario.models import Cliente
from pedido.models import Pedido, ItemPedido

from catalogo.tests.test_model import get_fake_produto
from usuario.tests.test_model import get_fake_endereco, get_fake_user
from catalogo.models import Cor, Modelo, ModeloProduto, Tamanho


class PedidoModelTest(TestCase):
    def setUp(self):
        self.obj = get_fake_pedido()

    def test_create(self):
        self.assertTrue(Pedido.objects.exists())


class ItemPedidoModelTest(TestCase):
    def setUp(self):
        pedido = get_fake_pedido()
        produto = get_fake_produto()
        modelo = Modelo.objects.create(descricao='T-Shirt')
        modelo_produto = ModeloProduto.objects.create(
            produto=produto, modelo=modelo)


        cor = Cor.objects.create(nome='Roxo', )
        tamanho = Tamanho.objects.create(nome='G', )

        self.obj = ItemPedido.objects.create(
            pedido=pedido,
            produto=produto,
            tamanho=tamanho,
            cor=cor,
            modelo_produto=modelo_produto
        )

    def test_create(self):
        self.assertTrue(ItemPedido.objects.exists())
    
    def test_str(self):
        self.assertEqual('Camiseta NodeJs', str(self.obj))


def get_fake_pedido():
    user = get_fake_user('ronaldo', 'ronaldo@likeestampa.com.br')
    cliente = Cliente.objects.get(user=user)
    endereco_cliente = get_fake_endereco(cliente)
    return Pedido.objects.create(
        user=user,
        endereco_cliente=endereco_cliente,
        request_seller='{"delivery_method_id": 90689, "order_id": 6, "customer_name": "Ronaldo Nazario", "customer_document": "92484291060", "customer_email": "ronaldo@gmail.com", "webhook_url": "https://option_webhook_url.com", "items": [{"name": "Camiseta For\u00e7a", "sku": "ideograma-forca", "qty": 1, "dimona_sku_id": 999999999, "designs": ["http://res.cloudinary.com/leonardocintra/image/upload/NAO_INFORMADO"], "mocks": ["http://res.cloudinary.com/leonardocintra/image/upload/v1624842615/bgue0uopz62i0m9r1hmo.jpg"]}], "address": {"street": "Avenida Doutor Severino Marcio Pereira Meirelles", "number": "1480", "complement": "", "city": "Franca", "state": "SP", "zipcode": "14408114", "neighborhood": "Villagio Mundo Novo", "phone": "8329382989", "country": "BR"}}'
    )
