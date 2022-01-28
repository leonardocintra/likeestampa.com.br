import json
from django.test import TestCase, Client
from django.test.utils import override_settings
from django.urls import reverse as r
from checkout.tests.test_model import get_fake_carrinho_com_items, UUID_FAKE_CARRINHO
from evento.models import EventoPedido
from pedido.models import Pedido
from usuario.tests.test_model import get_fake_endereco, get_fake_user
from usuario.models import Cliente
from evento.tests.test_model import create_fakes_status
from pedido.tests.test_model import get_fake_pedido
from pagamento.models import PagamentoMercadoPago


class PagamentoViewNaoAutenticado(TestCase):
    def setUp(self):
        self.client = Client()

    def test_usuario_nao_autenticado(self):
        response = self.client.get(r('pagamento:pagamento'))
        self.assertTrue(200, response.status_code)
        self.assertRedirects(response, '/accounts/login/?next=/pagamento/')


class PagamentoViewTest(TestCase):
    def setUp(self):
        get_fake_carrinho_com_items()
        create_fakes_status()
        self.client = Client()
        self.user = get_fake_user()
        cliente = Cliente.objects.get(user=self.user)
        get_fake_endereco(cliente)
        self.client.login(username='leonardo', password='123kkkuuu#')

    def test_carrinho_nao_esta_na_session(self):
        response = self.client.get(r('pagamento:pagamento'))
        self.assertTrue(200, response.status_code)
        self.assertRedirects(response, r('core:index'))
        self.assertRedirects(response, '/')

    def test_pagamento(self):
        Pedido.objects.all().delete()
        session = self.client.session
        session['carrinho'] = UUID_FAKE_CARRINHO
        session.save()

        response = self.client.get(r('pagamento:pagamento'))
        self.assertTrue(200, response.status_code)
        self.assertEqual(1, Pedido.objects.count())
    
    def test_pagamento_refresh_mais_de_uma_x_nao_pode_criar_novo_pedido(self):
        Pedido.objects.all().delete()
        EventoPedido.objects.all().delete()

        session = self.client.session
        session['carrinho'] = UUID_FAKE_CARRINHO
        session.save()

        response = self.client.get(r('pagamento:pagamento'))
        self.assertTrue(200, response.status_code)
        self.assertEqual(1, Pedido.objects.count())
        response = self.client.get(r('pagamento:pagamento'))
        self.assertTrue(200, response.status_code)
        self.assertEqual(1, Pedido.objects.count())
        response = self.client.get(r('pagamento:pagamento'))
        self.assertTrue(200, response.status_code)
        self.assertEqual(1, Pedido.objects.count())
        self.assertEqual(1, EventoPedido.objects.count())


class MpNotificationsTest(TestCase):
    def setUp(self):
        self.client = Client()

    @override_settings(DEBUG=True)
    def test_notificacao_mp_ipn_pagamento_nao_encontrado(self):
        response = self.client.post(
            r('pagamento:mp_notifications') + '?topic=payment&id=123456789')
        self.assertJSONEqual(response.content, {"pagamento": "nao-encontrado"})
        self.assertEqual(200, response.status_code)

    @override_settings(DEBUG=True)
    def test_notificacao_mp_ipn_status_approved(self):
        pedido = get_fake_pedido()
        PagamentoMercadoPago.objects.create(
            pedido=pedido,
            mercado_pago_id='qualquercoisa',
            payment_id=1240157386,
        )
        response = self.client.post(
            r('pagamento:mp_notifications') + '?topic=payment&id=1240157386')
        self.assertJSONEqual(response.content, {"pagamento": "aprovado"})
        self.assertEqual(201, response.status_code)

    @override_settings(DEBUG=True)
    def test_notificacao_mp_webhook_pagamento_nao_encontrado(self):
        data = {
            "id": 16965220292,
            "live_mode": False,
            "type": "payment",
            "date_created": "2015-03-25T10:04:58.396-04:00",
            "application_id": 123123123,
            "user_id": 44444,
            "version": 1,
            "api_version": "v1",
            "action": "payment.created",
            "data": {
                "id": "999999999"
            }
        }
        response = self.client.post(
            r('pagamento:webhook'), json.dumps(data), "application/json")
        self.assertJSONEqual(response.content, {"pagamento": "nao-encontrado"})
        self.assertEqual(200, response.status_code)
