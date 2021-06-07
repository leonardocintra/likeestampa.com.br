from django.contrib import admin
from .models import Categoria, SubCategoria, Produto, ProdutoImagem, Variacao, ProdutoVariacao


class VariacaoAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'ativo', ]


class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}


class SubCategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo', ]
    prepopulated_fields = {'slug': ('nome',)}


class ProdutoImagemInline(admin.TabularInline):
    model = ProdutoImagem
    extra = 5


class ProdutoVariacaoInline(admin.TabularInline):
    model = ProdutoVariacao
    extra = 4


class ProdutoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}
    list_display = ['nome', 'subcategoria', 'ativo', 'genero', ]
    inlines = [ProdutoImagemInline, ProdutoVariacaoInline]


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(SubCategoria, SubCategoriaAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Variacao, VariacaoAdmin)
