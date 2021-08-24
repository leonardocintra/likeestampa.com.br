from django.contrib.auth import authenticate, login
from django.urls import reverse as r
from django.test import TestCase, Client
from pagamento.models import PagamentoMercadoPago

from checkout.tests.test_model import get_fake_carrinho_com_items, UUID_FAKE_CARRINHO
from pedido.tests.test_model import get_fake_pedido
from usuario.tests.test_model import get_fake_user
from evento.tests.test_model import create_fakes_status


class PedidoFinalizadoMercadoPagoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_fake_user()
        self.client.login(username='leonardo', password='123kkkuuu#')

    def test_session_mercado_pago_id_not_found(self):
        session = self.client.session
        pedido = '123456'
        session['pedido'] = pedido
        session.save()
        response = self.client.get(r('pedido:pedido_finalizado_mercado_pago'))
        self.assertTrue(200, response.status_code)
        self.assertRedirects(response, r('pedido:pedido', kwargs={
                             'pk': pedido}), status_code=302, target_status_code=302, fetch_redirect_response=True)
    
    def test_pagamento_nao_pago_mercado_pago(self):
        get_fake_carrinho_com_items()
        create_fakes_status()

        session = self.client.session
        mercado_pago_id = '4990865-858e7361-f82b-4bdf-9532-16741d9d2a34'
        session['mercado_pago_id'] = mercado_pago_id
        session['carrinho'] = UUID_FAKE_CARRINHO
        session.save()
        pedido = get_fake_pedido()

        PagamentoMercadoPago.objects.create(
            pedido=pedido,
            mercado_pago_id=mercado_pago_id,
            payment_id=1240048121,
        )

        response = self.client.get('/pedido/pedido_finalizado_mercado_pago?collection_id=1240048121&collection_status=pending&payment_id=1240048121&status=pending&external_reference=LIKEESTAMPA-6&payment_type=ticket&merchant_order_id=3137638460&preference_id=4990865-ffad76a2-51c2-48d1-87fc-c5d00f169204&site_id=MLB&processing_mode=aggregator&merchant_account_id=null')
        self.assertTrue(200, response.status_code)
