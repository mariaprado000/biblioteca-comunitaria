from django.contrib import admin
from .models import Funcionario

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cargo', 'salario', 'data_admissao', 'ativo', 'criado_em')
    list_filter = ('cargo', 'ativo', 'data_admissao', 'criado_em')
    search_fields = ('usuario__first_name', 'usuario__last_name', 'cargo')
    list_editable = ('ativo',)
