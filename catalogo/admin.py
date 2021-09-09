from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin, NestedTabularInline
from catalogo.models import ModeloVariacao
from .models import Categoria, SubCategoria, Produto, Variacao, TipoVariacao, ModeloProduto, Modelo, Cor


class CorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}


class VariacaoAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'ativo', ]


class TipoVariacaoAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'variacao', 'ativo', 'valor_adicional', ]


class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}


class SubCategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo', ]
    prepopulated_fields = {'slug': ('nome',)}


class ProdutoVariacaoInline(NestedTabularInline):
    model = ModeloVariacao
    extra = 5
    fk_name = 'modelo_produto'


class ModeloProdutoInline(NestedStackedInline):
    model = ModeloProduto
    extra = 1
    fk_name = 'produto'
    inlines = [ProdutoVariacaoInline, ]


@admin.action(description='Ativar produtos')
def ativar_produtos(modeladmin, request, queryset):
    queryset.update(ativo=True)


@admin.action(description='Desativar produtos')
def desativar_produtos(modeladmin, request, queryset):
    queryset.update(ativo=False)


class ProdutoAdmin(NestedModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ['nome', ]
    list_filter = ['ativo', 'subcategoria', 'genero', ]
    list_display = ['nome', 'subcategoria', 'ativo', 'genero', 'modelo', ]
    inlines = [ModeloProdutoInline, ]

    actions = [ativar_produtos, desativar_produtos, ]

    @admin.display()
    def modelo(self, obj):
        # TODO: cachear
        modelo = ModeloProduto.objects.get(produto_id=obj.pk)
        return modelo


class ModeloAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'descricao_cliente', ]
    search_fields = ['descricao', ]


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Modelo, ModeloAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(SubCategoria, SubCategoriaAdmin)
admin.site.register(TipoVariacao, TipoVariacaoAdmin)
admin.site.register(Variacao, VariacaoAdmin)
admin.site.register(Cor, CorAdmin)
