from django import forms


class ProdutoDetalheForm(forms.Form):
    tamanho = forms.IntegerField()
    cor = forms.IntegerField()
    modelo = forms.CharField()
    quantidade = forms.IntegerField(max_value=10, min_value=1)
