from django.test import TestCase
from django.shortcuts import resolve_url as r


class AboutViewTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('core:about'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'about.html')

    def test_carrinho_link(self):
        expected = 'href="{}"'.format(r('checkout:carrinho'))
        self.assertContains(self.response, expected)

    def test_home_link(self):
        expected = 'href="{}"'.format(r('core:index'))
        self.assertContains(self.response, expected)
