import csv
import io
from django.http import HttpResponse
from django.test import TestCase
from apps.catalogo.utils.facebook_export import facebook_produtos_csv

fixtures_geral = [
    'fixtures/seller/seller.json',
    'fixtures/catalogo/subcategoria.json',
    'fixtures/catalogo/modelo.json',
    'fixtures/catalogo/produtos.json',
    'fixtures/catalogo/modelo_produto.json',
    'fixtures/catalogo/cor.json',
    'fixtures/catalogo/cor_modelo.json',
    'fixtures/catalogo/tamanho.json',
    'fixtures/catalogo/tamanho_modelo.json',
    'fixtures/catalogo/tipo_produto.json',
    'fixtures/catalogo/produto_imagens.json',
]


class FacebookExportTest(TestCase):
    fixtures = fixtures_geral

    def setUp(self) -> None:
        self.response = facebook_produtos_csv()

    def test_response_200(self):
        self.assertIsInstance(self.response, HttpResponse)
        self.assertEqual(200, self.response.status_code)

    def test_titulo_uppercase_contem_camiseta_antes(self):
        self.assertIsNotNone(self.response)

    def test_export_csv(self):
        content = self.response.content.decode('utf-8')
        cvs_reader = csv.reader(io.StringIO(content))
        body = list(cvs_reader)
        headers = body.pop(0)
        # validar se as celulas-titulo do csv obrigatorias estao presentes
        self.assertTrue('id' in headers)
        self.assertTrue('title' in headers)
        self.assertTrue('description' in headers)
        self.assertTrue('availability' in headers)
        self.assertTrue('condition' in headers)
        self.assertTrue('price' in headers)
        self.assertTrue('link' in headers)
        self.assertTrue('image_link' in headers)
        self.assertTrue('brand' in headers)
        self.assertTrue('additional_image_link' in headers)
        self.assertTrue('fb_product_category' in headers)
        self.assertTrue('material' in headers)

        # validar se o __titulo_item esta fazendo seu papel
        upper_test = body.pop(0)
        self.assertTrue('Camiseta GRPC' in upper_test)
