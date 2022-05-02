from django import template
from django.templatetags.static import static
from catalogo.models import TipoProduto

register = template.Library()


@register.simple_tag(name='imagem_tipo_produto')
def imagem_tipo_produto(tipo_produto_id=1):
    # para incluir a imagem aqui precisa adicionar manualmente na pasta core/static/img
    tipos_produto = TipoProduto.get_tipos_produto_ativo()
    imagem = tipos_produto.filter(id=tipo_produto_id).first()
    return static('img/' + imagem.icone_fontawesome + '.gif')
