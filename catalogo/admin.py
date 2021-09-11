from django.contrib import admin
from .models import Categoria, SubCategoria, Produto, ModeloProduto, Modelo, Cor, Tamanho, ProdutoImagem


class TamanhoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}
    list_display = ['nome', 'ativo', 'order_exibicao', ]


class CorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}
    list_display = ['nome', 'ativo', 'order_exibicao', 'valor',  ]


class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}


class SubCategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo', ]
    prepopulated_fields = {'slug': ('nome',)}


@admin.action(description='Ativar produtos')
def ativar_produtos(modeladmin, request, queryset):
    queryset.update(ativo=True)


@admin.action(description='Desativar produtos')
def desativar_produtos(modeladmin, request, queryset):
    queryset.update(ativo=False)


class ProdutoImagemInline(admin.TabularInline):
    model = ProdutoImagem

class ModeloProdutoInline(admin.TabularInline):
    model = ModeloProduto
    extra = 1


class ProdutoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ['nome', ]
    list_filter = ['ativo', 'subcategoria', 'genero', ]
    list_display = ['nome', 'subcategoria', 'ativo', 'genero', ]
    inlines = [ModeloProdutoInline, ProdutoImagemInline, ]

    actions = [ativar_produtos, desativar_produtos, ]


class ModeloAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'descricao_cliente', ]
    search_fields = ['descricao', ]


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Modelo, ModeloAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(SubCategoria, SubCategoriaAdmin)
admin.site.register(Cor, CorAdmin)
admin.site.register(Tamanho, TamanhoAdmin)
