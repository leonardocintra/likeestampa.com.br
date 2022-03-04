from django.contrib import admin
from .models import Cliente


class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome_cliente', 'cpf',]
    readonly_fields = ('user',)

    @admin.display()
    def nome_cliente(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name


admin.site.register(Cliente, ClienteAdmin)
