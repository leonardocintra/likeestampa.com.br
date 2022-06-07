from django.test import TestCase
from pagamento.models import PagamentoMercadoPago
from pedido.tests.test_model import get_fake_pedido


class PagamentoMercadoPagoModelTest(TestCase):
    def setUp(self):
        pedido = get_fake_pedido()
        self.obj = PagamentoMercadoPago.objects.create(
            pedido=pedido,
            mercado_pago_id='823948asakfjaslkjfalssasa',
            payment_id=8948299992,
        )

    def test_create(self):
        self.assertTrue(PagamentoMercadoPago.objects.exists())

    def test_str(self):
        self.assertTrue('823948asakfjaslkjfalssasa', str(self.obj))
