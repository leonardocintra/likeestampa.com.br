from django.test import TestCase
from evento.models import Status, EventoPedido, criar_evento
from pedido.models import Pedido
from pedido.tests.test_model import get_fake_pedido


class StatusModelTest(TestCase):
    def setUp(self):
        create_fakes_status()
        self.obj = Status.objects.get(id=5)
    
    def tearDown(self):
        Status.objects.all().delete()

    def test_create(self):
        self.assertTrue(Status.objects.exists())

    def test_str(self):
        self.assertEqual('Pedido entregue', str(self.obj))


class EventoPedidoModelTest(TestCase):
    def setUp(self):
        create_fakes_status()
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



def create_fakes_status():
    Status.objects.create(id=1, descricao='Pedido Recebido')
    Status.objects.create(id=2, descricao='Pedido Pago')
    Status.objects.create(id=3, descricao='Pedido em produção')
    Status.objects.create(id=4, descricao='Pedido em rota de entrega')
    Status.objects.create(id=5, descricao='Pedido entregue')
    Status.objects.create(id=6, descricao='Aguardando pagamento')
    Status.objects.create(id=7, descricao='Pedido Cancelado')
