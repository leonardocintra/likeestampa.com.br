from django.contrib import admin
from .models import PagamentoMercadoPago, PagamentoMercadoPagoWebhook


class PagamentoMercadoPagoWebhookAdmin(admin.ModelAdmin):
    list_display = ['mercado_pago', 'webhook_executado', 'webhook_data_recebimento', ]
    readonly_fields = ['mercado_pago', 'webhook_request', ]


class PagamentoMercadoPagoAdmin(admin.ModelAdmin):
    list_display = ['mercado_pago_id', 'mercado_pago_status', ]
    search_fields = ['mercado_pago_id']
    readonly_fields = ('pedido', 'mercado_pago_id', 'payment_method_id', 'transaction_amount', 'installments',
                       'mercado_pago_status', 'mercado_pago_status_detail', 'mercado_pago_id',)


admin.site.register(PagamentoMercadoPagoWebhook, PagamentoMercadoPagoWebhookAdmin)
admin.site.register(PagamentoMercadoPago, PagamentoMercadoPagoAdmin)
