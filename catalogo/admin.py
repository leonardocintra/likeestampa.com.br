from django.contrib import admin
from sentry_sdk import capture_exception

from catalogo.utils.facebook_export import facebook_produtos_csv

from .models import (TipoProduto, SubCategoria, Produto, ModeloProduto,
                     Modelo, Cor, Tamanho, ProdutoImagem, TamanhoModelo, CorModelo)


class TamanhoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}
    list_display = ['nome', 'id', 'ativo',
                    'order_exibicao', 'descricao_cliente', ]


class CorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}
    list_display = ['nome', 'ativo', 'order_exibicao', 'valor', ]


class TipoProdutoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}
    list_display = ['nome', 'icone_fontawesome', 'ativo', ]


class SubCategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo', ]
    prepopulated_fields = {'slug': ('nome',)}


@admin.action(description='Ativar produtos')
def ativar_produtos(modeladmin, request, queryset):
    queryset.update(ativo=True)


@admin.action(description='Desativar produtos')
def desativar_produtos(modeladmin, request, queryset):
    queryset.update(ativo=False)


@admin.action(description='Download CSV Produtos')
def download_csv(self, request, queryset):
    return facebook_produtos_csv()


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
    actions = [ativar_produtos, desativar_produtos, download_csv, ]

    def save_model(self, request, obj, form, change):
        saved = super().save_model(request, obj, form, change)

        # Caso for selecionado os modelos, nao faz o cadastro manualmente
        if form.data['modelo_produto-INITIAL_FORMS'] != '0':
            return saved

        try:
            tshirt = Modelo.objects.get(descricao='T-Shirt')
            babylong = Modelo.objects.get(descricao='Baby Long')
            infantil = Modelo.objects.get(descricao='Classic Infantil')

            ModeloProduto.objects.create(produto=obj, modelo=tshirt)
            ModeloProduto.objects.create(produto=obj, modelo=babylong)
            ModeloProduto.objects.create(produto=obj, modelo=infantil)
        except Exception as e:
            capture_exception(e)
            print('Erro no cadastro do produto')

        return saved


class ModeloAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'descricao_cliente',
                    'tipo_produto', 'valor', 'slug', ]
    search_fields = ['descricao', ]
    prepopulated_fields = {'slug': ('descricao',)}


class TamanhoModeloAdmin(admin.ModelAdmin):
    pass


class CorModeloAdmin(admin.ModelAdmin):
    list_display = ['cor', 'modelo', 'ativo']


admin.site.register(TipoProduto, TipoProdutoAdmin)
admin.site.register(Modelo, ModeloAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(SubCategoria, SubCategoriaAdmin)
admin.site.register(Cor, CorAdmin)
admin.site.register(Tamanho, TamanhoAdmin)
admin.site.register(TamanhoModelo, TamanhoModeloAdmin)
admin.site.register(CorModelo, CorModeloAdmin)
