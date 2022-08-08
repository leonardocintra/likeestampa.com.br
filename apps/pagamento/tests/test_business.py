from django.test import TestCase, override_settings
from apps.checkout.models import Carrinho
from apps.checkout.tests.test_model import UUID_FAKE_CARRINHO, get_fake_carrinho_com_items
from apps.pagamento.models import PagamentoMercadoPago

from apps.pedido.business import concluir_pedido
from apps.pedido.models import ItemPedido, Pedido
from apps.pedido.tests.test_model import get_fake_pedido


@override_settings(DEBUG=True)
class ConcluirPedidoTest(TestCase):
    fixtures = [
        'fixtures/evento/status.json',
        'fixtures/catalogo/tipo_produto.json',
    ]

    def setUp(self):
        Pedido.objects.all().delete()
        ItemPedido.objects.all().delete()
        Carrinho.objects.all().delete()
        self.pedido = get_fake_pedido()
        PagamentoMercadoPago.objects.create(
            pedido=self.pedido,
            mercado_pago_id='823948asakfjaslkjfalssasa',
            payment_id=1240157386,
        )
        get_fake_carrinho_com_items()
        Carrinho.objects.filter(
            uuid=UUID_FAKE_CARRINHO).update(pedido=self.pedido)
        concluir_pedido(self.pedido, 1240157386)

    def test_pedido_existe(self):
        self.assertEqual(1, Pedido.objects.count())

    def test_pedido_seller_foi_gerado(self):
        self.assertIsNotNone(self.pedido.request_seller)

    def test_items_do_pedido_criados(self):
        items = ItemPedido.objects.filter(pedido=self.pedido)
        self.assertEqual(len(items), ItemPedido.objects.count())

    def test_carrinho_foi_deletado(self):
        self.assertEqual(0, Carrinho.objects.count())
