from django import forms


class FreteForm(forms.Form):
    # Frete do DIMONA
    delivery_method_id = forms.IntegerField(min_value=1)
