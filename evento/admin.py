from django.contrib import admin
from .models import Status


class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao', 'visivel_cliente', ]
    list_filter = ['visivel_cliente', ]
    search_fields = ['descricao', ]


admin.site.register(Status, StatusAdmin)
