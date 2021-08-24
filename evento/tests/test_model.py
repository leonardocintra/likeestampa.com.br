from django.test import TestCase
from evento.models import Status, EventoPedido


class StatusModelTest(TestCase):
    def setUp(self):
        create_fakes_status()
        self.obj = Status.objects.get(id=5)

    def test_create(self):
        self.assertTrue(Status.objects.exists())

    def test_str(self):
        self.assertEqual('Pedido entregue', str(self.obj))


def create_fakes_status():
    Status.objects.create(id=1, descricao='Pedido Recebido')
    Status.objects.create(id=2, descricao='Pedido Pago')
    Status.objects.create(id=3, descricao='Pedido em produção')
    Status.objects.create(id=4, descricao='Pedido em rota de entrega')
    Status.objects.create(id=5, descricao='Pedido entregue')
    Status.objects.create(id=6, descricao='Aguardando pagamento')
    Status.objects.create(id=7, descricao='Pedido Cancelado')
