from services.mailgun.email import envia_email_de_teste
from django.contrib import admin
from .models import Pedido


@admin.action(description='Envia email pedido pago')
def envia_email_teste(modeladmin, request, queryset):
    envia_email_de_teste()


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'pago', 'nome_cliente',
                    'created_at', 'pedido_seller', ]
    search_fields = ['id', ]
    list_filter = ['pago', 'gateway_pagamento', ]
    readonly_fields = ['id', 'user', 'valor_total', 'endereco_cliente', 'valor_frete', 'request_seller',
                       'valor_items', 'frete_id', 'gateway_pagamento', ]

    actions = [envia_email_teste, ]

    def save_model(self, request, obj, form, change):
        if obj.pago:
            print('Voce esta pagando!')
        return super().save_model(request, obj, form, change)

    @admin.display()
    def nome_cliente(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name
