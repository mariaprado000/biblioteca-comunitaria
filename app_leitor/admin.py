from django.contrib import admin
from .models import Leitor

@admin.register(Leitor)
class LeitorAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'cpf', 'telefone', 'ativo', 'criado_em')
    list_filter = ('ativo', 'criado_em')
    search_fields = ('first_name', 'last_name', 'cpf', 'telefone')
    list_editable = ('ativo',)
