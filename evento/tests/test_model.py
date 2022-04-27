from datetime import datetime
from django.utils import timezone
from django.test import TestCase
from evento.models import Status, EventoPedido, criar_evento
from pedido.models import Pedido
from pedido.tests.test_model import get_fake_pedido


class StatusModelTest(TestCase):
    fixtures = ['fixtures/evento/status.json', ]
    
    def setUp(self):
        self.obj = Status.objects.get(id=5)
    
    def tearDown(self):
        Status.objects.all().delete()

    def test_create(self):
        self.assertTrue(Status.objects.exists())

    def test_str(self):
        self.assertEqual('Pedido entregue', str(self.obj))


class EventoPedidoModelTest(TestCase):

    fixtures = ['fixtures/evento/status.json', ]

    def setUp(self):
        self.pedido = get_fake_pedido()
        self.status = Status.objects.get(pk=1)
    
    def tearDown(self):
        Pedido.objects.all().delete()
        Status.objects.all().delete()
    
    def test_create(self):
        EventoPedido.objects.create(evento=self.status, pedido=self.pedido)
        self.assertTrue(EventoPedido.objects.exists())
    
    def test_nao_deixar_criar_pedidos_duplicados(self):
        criar_evento(1, self.pedido)
        self.assertEqual(1, EventoPedido.objects.count())
        criar_evento(2, self.pedido)
        self.assertEqual(2, EventoPedido.objects.count())
        criar_evento(3, self.pedido)
        self.assertEqual(3, EventoPedido.objects.count())
        # Tenta criar novamento um pedido com evento 3
        criar_evento(3, self.pedido)
        self.assertEqual(3, EventoPedido.objects.count())
        # Aceita criar um novo separado
        criar_evento(4, self.pedido)
        self.assertEqual(4, EventoPedido.objects.count())
        # Tenta criar novamento um pedido com evento 3
        criar_evento(3, self.pedido)
        self.assertEqual(4, EventoPedido.objects.count())
    
    def test_data_ocorrencia(self):
        criar_evento(1, self.pedido)
        evento = EventoPedido.objects.get(pedido=self.pedido)
        self.assertIsNotNone(evento)
        self.assertIsNone(evento.data_ocorrencia)
        datetime.now()
        EventoPedido.objects.filter(pedido=self.pedido).update(data_ocorrencia=datetime.now(tz=timezone.utc))
        evento = EventoPedido.objects.get(pedido=self.pedido)
        self.assertIsNotNone(evento.data_ocorrencia)
