from django.test import TestCase, Client
from django.urls import reverse as r
from checkout.tests.test_model import get_fake_carrinho_com_items, UUID_FAKE_CARRINHO
from usuario.tests.test_model import get_fake_endereco, get_fake_user
from usuario.models import Cliente
from evento.tests.test_model import create_fakes_status


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
        session = self.client.session
        session['carrinho'] = UUID_FAKE_CARRINHO
        session.save()
        
        response = self.client.get(r('pagamento:pagamento'))
        self.assertTrue(200, response.status_code)
