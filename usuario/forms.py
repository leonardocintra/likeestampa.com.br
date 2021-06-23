from django import forms
from django.forms import ModelForm
from .models import Cliente
from services.peoplesoft.peoplesoft import cadastrar_cliente

SEXO = {
    ('M', 'Masculino'),
    ('F', 'Feminino'),
}


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
    uf = forms.CharField(label='UF', max_length=2, min_length=2)
    complemento = forms.CharField(max_length=100, required=False)
    referencia = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Cliente
        fields = ('nome', 'sobrenome', 'email', 'cpf')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['nome']
        user.last_name = self.cleaned_data['sobrenome']
        user.email = self.cleaned_data['email']
        user.save()

        user.cliente.cpf = self.cleaned_data['cpf']
        peoplesoft_id = cadastrar_cliente(self.cleaned_data)
        user.cliente.peoplesoft_id = peoplesoft_id
        user.cliente.save()
