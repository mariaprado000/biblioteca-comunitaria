from django.contrib import admin
from .models import Funcionario

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'cargo', 'salario', 'data_admissao', 'ativo', 'criado_em')
    list_filter = ('cargo', 'ativo', 'data_admissao', 'criado_em')
    search_fields = ('first_name', 'last_name', 'cargo')
    list_editable = ('ativo',)
