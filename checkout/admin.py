from django.contrib import admin
from .models import Carrinho


class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'abandonado', 'created_at']


admin.site.register(Carrinho, CarrinhoAdmin)
