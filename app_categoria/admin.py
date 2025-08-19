from django.contrib import admin
from .models import Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'criado_em')
    list_filter = ('criado_em',)
    search_fields = ('nome', 'descricao')
