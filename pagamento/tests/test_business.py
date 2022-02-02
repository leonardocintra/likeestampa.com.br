from django.test import TestCase, override_settings
from checkout.models import Carrinho
from checkout.tests.test_model import UUID_FAKE_CARRINHO, get_fake_carrinho_com_items
from evento.tests.test_model import create_fakes_status
from pagamento.models import PagamentoMercadoPago

from pedido.business import concluir_pedido
from pedido.models import ItemPedido, Pedido
from pedido.tests.test_model import get_fake_pedido


class ConcluirPedidoTest(TestCase):
    def setUp(self):
        create_fakes_status()
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
        Carrinho.objects.filter(uuid=UUID_FAKE_CARRINHO).update(pedido=self.pedido)
        concluir_pedido(self.pedido, 1240157386)
    
    @override_settings(DEBUG=True)
    def test_pedido_existe(self):    
        self.assertEqual(1, Pedido.objects.count())
    
    @override_settings(DEBUG=True)
    def test_pedido_seller_foi_gerado(self):
        self.assertIsNotNone(self.pedido.request_seller)
    
    @override_settings(DEBUG=True)
    def test_items_do_pedido_criados(self):
        items = ItemPedido.objects.filter(pedido=self.pedido)
        self.assertEqual(len(items), ItemPedido.objects.count())
    
    @override_settings(DEBUG=True)
    def test_carrinho_foi_deletado(self):
        self.assertEqual(0, Carrinho.objects.count())
        
    
