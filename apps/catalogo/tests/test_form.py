from django.test import TestCase
from apps.catalogo.forms import ProdutoDetalheForm


class ProdutoDetalheFormTest(TestCase):
    def test_form_has_fields(self):
        form = ProdutoDetalheForm()
        expected = ['tamanho', 'cor', 'modelo', 'quantidade']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_quantidade_valor_maximo(self):
        form = self.criar_um_form_valido(quantidade=1000)
        self.assertFalse(form.is_valid())
        form = self.criar_um_form_valido(quantidade=4)
        self.assertTrue(form.is_valid())

    def test_quantidade_valor_minimo(self):
        form = self.criar_um_form_valido(quantidade=0)
        self.assertFalse(form.is_valid())
        form = self.criar_um_form_valido(quantidade=4)
        self.assertTrue(form.is_valid())

    def criar_um_form_valido(self, **kwargs):
        valid = dict(tamanho=1, cor=1,
                     modelo='Tradicional', quantidade=1)
        data = dict(valid, **kwargs)
        form = ProdutoDetalheForm(data)
        form.is_valid()
        return form
