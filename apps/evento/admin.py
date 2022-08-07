from django.contrib import admin
from .models import Status, EventoPedido


class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao', 'visivel_cliente', ]
    list_filter = ['visivel_cliente', ]
    search_fields = ['descricao', ]


class EventoPedidoAdmin(admin.ModelAdmin):
    list_display =['pedido', ]


admin.site.register(Status, StatusAdmin)
admin.site.register(EventoPedido, EventoPedidoAdmin)
