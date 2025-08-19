from django.contrib import admin
from .models import Livro

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'ano', 'disponivel', 'criado_em')
    list_filter = ('categoria', 'ano', 'disponivel', 'criado_em')
    search_fields = ('titulo', 'autor', 'isbn', 'editora')
    list_editable = ('disponivel',)
