from django.contrib import admin
from .models import Leitor

@admin.register(Leitor)
class LeitorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cpf', 'telefone', 'ativo', 'criado_em')
    list_filter = ('ativo', 'criado_em')
    search_fields = ('usuario__first_name', 'usuario__last_name', 'cpf', 'telefone')
    list_editable = ('ativo',)
