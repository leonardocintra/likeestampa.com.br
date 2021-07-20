from django.contrib import admin
from .models import Pedido


class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'pago', 'user_id', ]
    search_fields = ['id', ]
    list_filter = ['pago', 'gateway_pagamento', ]
    readonly_fields = ['id', 'user', 'valor_total',
                       'gateway_pagamento', ]


admin.site.register(Pedido, PedidoAdmin)
