from django.test import TestCase
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
        self.pedido = get_fake_pedido()
        PagamentoMercadoPago.objects.create(
            pedido=self.pedido,
            mercado_pago_id='823948asakfjaslkjfalssasa',
            payment_id=1240157386,
        )
    
    def test_pedido_existe(self):    
        concluir_pedido(self.pedido, 1240157386)
        self.assertEqual(1, Pedido.objects.count())
    
    def test_items_do_pedido_criados(self):
        items = ItemPedido.objects.filter(pedido=self.pedido)
        self.assertEqual(len(items), ItemPedido.objects.count())
        
    
