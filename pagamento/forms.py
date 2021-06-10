import mercadopago
from django import forms
from django.conf import settings
from .models import Pagamento


class PagamentoForm(forms.ModelForm):
    token = forms.CharField()

    class Meta:
        model = Pagamento
        fields = [
            'valor_pedido',
            'parcelas',
            'metodo_pagamento',
            'email',
            'numero_documento'
        ]

    def __init__(self, *args, **kwargs):
        self.pedido = kwargs.pop("pedido")
        super().__init__(*args, **kwargs)

    
    def limpar_valor_do_pedido(self):
        """ Para nao deixar o cara alterar o valor no HTML"""
        pass # https://github.com/fabioruicci/tutorial-e-commerce-django/blob/main/payments/forms.py#L25


    # parei aqui https://youtu.be/bAxEQBY9els?t=2646
    
