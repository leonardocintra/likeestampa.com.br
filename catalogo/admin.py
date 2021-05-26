from django.contrib import admin
from .models import Categoria, SubCategoria, Produto, ProdutoImagem


class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}


class SubCategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo', ]
    prepopulated_fields = {'slug': ('nome',)}


class ProdutoImagemInline(admin.TabularInline):
    model = ProdutoImagem
    extra = 5


class ProdutoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}
    list_display = ['nome', 'subcategoria', 'ativo', 'genero', ]
    inlines = [ProdutoImagemInline]


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(SubCategoria, SubCategoriaAdmin)
admin.site.register(Produto, ProdutoAdmin)
