from django.contrib import admin
from .models import Categoria, SubCategoria, Produto


class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}


class SubCategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}


class ProdutoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome',)}


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(SubCategoria, SubCategoriaAdmin)
admin.site.register(Produto, ProdutoAdmin)
