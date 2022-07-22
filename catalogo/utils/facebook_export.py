import csv
from django.http import HttpResponse

from catalogo.models import Produto, ProdutoImagem


def facebook_produtos_csv():
    filename = 'likeestampa-produtos.csv'
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=' + filename},
    )

    writer = csv.writer(response)
    writer.writerow(['id', 'title', 'description', 'availability', 'condition',
                    'price', 'link', 'image_link', 'brand', 'additional_image_link', 'material'])
    imagens = ProdutoImagem.objects.all()
    produtos = Produto.get_produtos_ativos()

    for p in produtos:
        writer.writerow([p.id, p, p.descricao, 'in stock', 'new', '51.90 BLR', 'https://www.likeestampa.com.br/catalogo/produto/' + p.slug,
                        p.imagem_principal.url, 'Like Estampa', __imagens_adicionais(imagens, p.id), '100% Algodão'])

    return response


def __imagens_adicionais(imagens, produto_id):
    imagens_adicionais = ''
    for img in imagens:
        if img.produto.id == produto_id:
            imagens_adicionais = imagens_adicionais + img.imagem.url + ','
    return imagens_adicionais
