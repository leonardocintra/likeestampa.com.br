from django import forms


class ProdutoDetalheForm(forms.Form):
    tamanho = forms.CharField()
    cor = forms.CharField()
    modelo = forms.CharField()
    quantidade = forms.IntegerField(max_value=10, min_value=1)
