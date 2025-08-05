from django.contrib import admin
from .models import Livro, Categoria

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'ano', 'genero', 'categoria', 'disponivel']
    list_filter = ['disponivel', 'genero', 'categoria']
    search_fields = ['titulo', 'autor', 'isbn']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'criado_em']
    search_fields = ['nome']
