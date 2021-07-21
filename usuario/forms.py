from django import forms
from django.forms import ModelForm
from localflavor.br.forms import BRCPFField
from core.constants import UF, SEXO
from .models import Cliente, EnderecoCliente


class ClienteForm(forms.Form):
    cpf = BRCPFField()
    nome = forms.CharField(label='Nome', max_length=100)
    sobrenome = forms.CharField(label='Sobrenome', max_length=100)
    email = forms.EmailField(label='E-mail', max_length=100)
    cep = forms.CharField(label='CEP', max_length=8, min_length=8)
    telefone = forms.CharField(max_length=9, min_length=5)


class EnderecoClienteForm(forms.Form):
    endereco = forms.CharField(label='Endereço', max_length=100)
    numero = forms.CharField(label='Nº', max_length=100)
    complemento = forms.CharField(
        label='Complemento', max_length=100, required=False)
    bairro = forms.CharField(label='Bairro', max_length=100)
    cidade = forms.CharField(label='Cidade', max_length=100)
    uf = forms.CharField(label='UF', max_length=100)
    referencia = forms.CharField(
        label='Referencia', max_length=100, required=False)


class SignupForm(forms.ModelForm):
    cpf = forms.CharField(label='CPF', max_length=11, min_length=11)
    nome = forms.CharField(max_length=50)
    sobrenome = forms.CharField(max_length=50)
    sexo = forms.ChoiceField(choices=SEXO)
    email = forms.EmailField()
    cep = forms.CharField(label='CEP', max_length=8, min_length=8)
    endereco = forms.CharField(max_length=100)
    bairro = forms.CharField(max_length=100)
    numero = forms.CharField(max_length=8)
    cidade = forms.CharField(max_length=100)
    uf = forms.ChoiceField(choices=UF)
    complemento = forms.CharField(max_length=100, required=False)
    referencia = forms.CharField(max_length=100, required=False)
    telefone = forms.CharField(max_length=12, min_length=9)

    class Meta:
        model = Cliente
        fields = ('nome', 'sobrenome', 'email', 'cpf')

    def signup(self, request, user):
        cliente = self.cleaned_data

        # Cria o usuario
        user.first_name = cliente['nome']
        user.last_name = cliente['sobrenome']
        user.email = cliente['email']
        user.save()

        # Cria o cliente
        user.cliente.cpf = cliente['cpf']
        user.cliente.telefone = cliente['telefone']
        user.cliente.save()
        EnderecoCliente.objects.create(
            cliente=user.cliente,
            cep=cliente['cep'],
            endereco=cliente['endereco'],
            numero=cliente['numero'],
            bairro=cliente['bairro'],
            cidade=cliente['cidade'],
            uf=cliente['uf'],
            referencia=cliente['referencia'],
            complemento=cliente['complemento'],
        )
