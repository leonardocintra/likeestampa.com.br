from django import forms
from django.forms import ModelForm
from localflavor.br.forms import BRCPFField
from core.constants import UF


class FreteForm(forms.Form):
    # Frete do DIMONA
    delivery_method_id = forms.IntegerField(min_value=1)

