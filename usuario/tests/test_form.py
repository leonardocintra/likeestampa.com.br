from django.test import TestCase
from usuario.models import Cliente, EnderecoCliente
from usuario.forms import SignupForm


class SignupFormTest(TestCase):
    def test_form_has_fields(self):
        form = SignupForm()
        expected = ['nome', 'sobrenome', 'email', 'cpf', 'sexo', 'cep', 'endereco', 'bairro',
                    'numero', 'cidade', 'uf', 'complemento', 'referencia', 'telefone', ]
        self.assertSequenceEqual(expected, list(form.fields))

    def test_cpf_tem_11_digitos(self):
        pass
