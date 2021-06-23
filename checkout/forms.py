from django import forms
from django.forms import ModelForm
from localflavor.br.forms import BRCPFField


class ClienteForm(forms.Form):
    # TODO: migrar para a app usuario
    cpf = BRCPFField()
    nome = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='E-mail', max_length=100)
    cep = forms.CharField(label='CEP', max_length=8, min_length=8)
    endereco = forms.CharField(label='Endereço', max_length=100)
    numero = forms.CharField(label='Nº', max_length=100)
    complemento = forms.CharField(
        label='Complemento', max_length=100, required=False)
    bairro = forms.CharField(label='Bairro', max_length=100)
    cidade = forms.CharField(label='Cidade', max_length=100)
    uf = forms.CharField(label='UF', max_length=100)
    referencia = forms.CharField(
        label='Referencia', max_length=100, required=False)