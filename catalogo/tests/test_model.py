from django.test import TestCase
from catalogo.models import Categoria


class CategoriaModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Categoria.objects.create(nome='Camisetas', slug='camiseta')

    def test_slug_label(self):
        categoria = Categoria.objects.get(id=1)
        field_label = categoria._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'Identificador')

    def test_created_at_label(self):
        categoria = Categoria.objects.get(id=1)
        field_label = categoria._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'Criado em')

    def test_updated_at_label(self):
        categoria = Categoria.objects.get(id=1)
        field_label = categoria._meta.get_field('updated_at').verbose_name
        self.assertEquals(field_label, 'Modificado em')

    def test_nome_max_length(self):
        categoria = Categoria.objects.get(id=1)
        max_length = categoria._meta.get_field('nome').max_length
        self.assertEquals(max_length, 100)

    def test_slug_max_length(self):
        categoria = Categoria.objects.get(id=1)
        max_length = categoria._meta.get_field('slug').max_length
        self.assertEquals(max_length, 100)

    def test_first_name_max_length(self):
        categoria = Categoria.objects.get(id=1)
        max_length = categoria._meta.get_field('nome').max_length
        self.assertEquals(max_length, 100)

    def test_ativo_default_true(self):
        categoria = Categoria.objects.get(id=1)
        ativo = categoria.ativo
        self.assertEquals(True, ativo)
