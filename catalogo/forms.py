from django import forms


class ProdutoDetalheForm(forms.Form):
    tamanho = forms.IntegerField()
    cor = forms.IntegerField()
    quantidade = forms.IntegerField(max_value=10, min_value=1)
