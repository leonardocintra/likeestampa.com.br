from django.test import TestCase, Client, override_settings
from django.urls import reverse
from checkout.models import Carrinho, ItemCarrinho

from checkout.tests.test_model import UUID_FAKE_CARRINHO, get_fake_carrinho_com_items
from checkout.forms import FreteForm


@override_settings(DEBUG=True)
class CarrinhoViewClienteNaoAutenticadoTest(TestCase):
    fixtures = [
        'fixtures/catalogo/tipo_produto.json',
    ]

    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse('checkout:carrinho'))

    def test_carrinho_vazio(self):
        quantidade_item = self.response.context['quantidade_item']
        valor_carrinho = self.response.context['valor_carrinho']
        self.assertEqual(0, Carrinho.objects.count())
        self.assertEqual(0, quantidade_item)
        self.assertEqual(0, valor_carrinho)
        self.assertEqual(200, self.response.status_code)
        self.assertContains(self.response, "Carrinho vazio")
        self.assertContains(
            self.response, "Adicione produtos para calular o frete")

    def test_template_correto(self):
        self.assertEqual(200, self.response.status_code)
        self.assertTemplateUsed(self.response, 'checkout/carrinho.html')

    def test_has_form_frete(self):
        form = self.response.context['form_frete']
        self.assertIsInstance(form, FreteForm)

    def test_aparecer_botao_login_e_cadastro(self):
        btn_login = '<a class="btn btn-success" href="/accounts/login/">Entrar </a>'
        btn_cadastro = '<a class="btn btn-primary" href="/accounts/signup/">Fazer cadastro</a>'
        label_quantidade_item_carrinho = '<span class="badge bg-primary rounded-pill">0</span>'
        self.assertContains(self.response, btn_login)
        self.assertContains(self.response, btn_cadastro)
        self.assertContains(self.response, label_quantidade_item_carrinho)

    def test_spinner_excluir_nao_existe_na_pagina_sem_item_carrinho(self):
        spinner = '<button class="btn btn-danger btn-sm btn-excluir-spinner" type="button" disabled id="btn-excluir-spinner-'
        self.assertNotContains(self.response, spinner)

    def test_spinner_excluir_existe_na_pagina_com_item_carrinho(self):
        get_fake_carrinho_com_items()
        session = self.client.session
        session['carrinho'] = UUID_FAKE_CARRINHO
        session.save()
        res = self.client.get(reverse('checkout:carrinho'))
        spinner = '<button class="btn btn-danger btn-sm btn-excluir-spinner" type="button" disabled id="btn-excluir-spinner-'
        self.assertContains(res, spinner)

    def test_dados_do_cliente_vazio(self):
        self.assertIsNone(self.response.context['enderecos'])
        self.assertIsNone(self.response.context['cliente'])
        self.assertEqual('', self.response.context['cep_padrao'])

    def test_carrinho_com_items(self):
        get_fake_carrinho_com_items()
        session = self.client.session
        session['carrinho'] = UUID_FAKE_CARRINHO
        session.save()
        res = self.client.get(reverse('checkout:carrinho'))
        quantidade_item = res.context['quantidade_item']
        valor_carrinho = res.context['valor_carrinho']
        label_quantidade_1_carrinho = '<span class="badge bg-primary rounded-pill">1</span>'

        self.assertEqual(1, Carrinho.objects.count())
        self.assertEqual(1, ItemCarrinho.objects.count())
        self.assertEqual(1, quantidade_item)
        self.assertEqual(47.90, float(valor_carrinho))
        self.assertContains(res, label_quantidade_1_carrinho)

    def test_calculo_frete(self):
        get_fake_carrinho_com_items()
        session = self.client.session
        session['carrinho'] = UUID_FAKE_CARRINHO
        session.save()
        res1 = self.client.post(reverse('checkout:carrinho'), data={
                                'calcular-frete': 37990000})
        self.assertEqual('37990000', res1.context['cep_padrao'])
        res2 = self.client.post(reverse('checkout:carrinho'), data={
                                'calcular-frete': 823899992})
        self.assertEqual('823899992', res2.context['cep_padrao'])
        self.assertEqual('frete-nao-encontrado', res2.context['frete_items'])
