from django.contrib import admin
from .models import Carrinho, ItemCarrinho


class ItemCarrinhoInline(admin.TabularInline):
    model = ItemCarrinho
    readonly_fields = ['cor', 'quantidade', 'tamanho', 'modelo_produto', 'produto',  ]


class CarrinhoAdmin(admin.ModelAdmin):
    readonly_fields = ['uuid', ]
    list_display = ['uuid', 'abandonado', 'created_at']
    inlines = [
        ItemCarrinhoInline,
    ]


admin.site.register(Carrinho, CarrinhoAdmin)
