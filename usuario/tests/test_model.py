from datetime import datetime
from django.test import TestCase
from usuario.models import Cliente, EnderecoCliente
from django.contrib.auth.models import User


class ClienteModelTest(TestCase):

    def setUp(self):
        user = User.objects.create_user(
            username='leonardo',
            first_name='Leonardo',
            email='leonardo@leonardo.com',
            password='123kkkuuu#')
        self.obj = Cliente.objects.get(user=user)

    def test_criacao_cliente(self):
        # ao criar um usuario a gente ja cria um Cliente
        self.assertTrue(Cliente.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Leonardo', str(self.obj))

    def test_cpf(self):
        self.assertEqual('', str(self.obj.cpf))

    def test_cpf(self):
        Cliente.objects.filter(pk=self.obj.pk).update(cpf='86528591083')
        cliente = Cliente.objects.get(pk=self.obj.pk)
        self.assertEqual('86528591083', cliente.cpf)

    def test_telefone(self):
        Cliente.objects.filter(pk=self.obj.pk).update(telefone='9887772727')
        cliente = Cliente.objects.get(pk=self.obj.pk)
        self.assertEqual('9887772727', cliente.telefone)


class EnderecoClienteModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='leonardo',
            first_name='Leonardo',
            email='leonardo@leonardo.com',
            password='123kkkuuu#')
        cliente = Cliente.objects.get(user=user)

        self.obj = EnderecoCliente(
            cliente=cliente,
            cep='37990000',
            endereco='Rua 6 de abril',
            numero='123',
            cidade='Ibiraci',
            uf='MG',
            bairro='Alto da Boa Vista'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(EnderecoCliente.objects.exists())

    def test_endereco_ativo(self):
        self.assertTrue(self.obj.ativo)

    def test_str(self):
        self.assertEqual('Rua 6 de abril', self.obj.endereco)

    def test_pais_default_value(self):
        self.assertEqual('Brasil', self.obj.pais)
