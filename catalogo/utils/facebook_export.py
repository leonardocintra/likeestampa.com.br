import csv
from tokenize import String
from django.http import HttpResponse

from catalogo.models import Produto, ProdutoImagem


def facebook_produtos_csv():
    filename = 'likeestampa-produtos.csv'
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=' + filename},
    )

    writer = csv.writer(response)
    writer.writerow(['id',
                    'title',
                     'description',
                     'availability',
                     'condition',
                     'price',
                     'link',
                     'image_link',
                     'brand',
                     'additional_image_link',
                     'fb_product_category'
                     'material'])
    imagens = ProdutoImagem.objects.all()
    produtos = Produto.get_produtos_ativos()

    for p in produtos:
        writer.writerow([p.id, p,
                        __titulo_item(p.descricao),
                        'in stock',
                         'new',
                         '51.90 BRL',
                         'https://www.likeestampa.com.br/catalogo/produto/' + p.slug,
                         p.imagem_principal.url,
                         'Like Estampa',
                         __imagens_adicionais(imagens, p.id),
                         'roupas e acessórios > roupas > roupas masculinas > camisas e camisetas'
                         '100% Algodão'])

    return response


def __titulo_item(nome_produto: String):
    if nome_produto.isupper():
        return 'Camiseta ' + nome_produto
    return nome_produto


def __imagens_adicionais(imagens, produto_id):
    imagens_adicionais = ''
    for img in imagens:
        if img.produto.id == produto_id:
            imagens_adicionais = imagens_adicionais + img.imagem.url + ','
    return imagens_adicionais
