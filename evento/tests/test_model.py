from django.test import TestCase
from evento.models import Status, EventoPedido


class StatusModelTest(TestCase):
    def setUp(self):
        self.obj = Status.objects.create(descricao='Pedido Entregue')

    def test_create(self):
        self.assertTrue(Status.objects.exists())

    def test_str(self):
        self.assertEqual('Pedido Entregue', str(self.obj))
