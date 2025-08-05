from django.contrib import admin
from .models import Leitor, Funcionario

@admin.register(Leitor)
class LeitorAdmin(admin.ModelAdmin):
    list_display = ['get_nome_completo', 'cpf', 'telefone', 'ativo']
    list_filter = ['ativo']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'cpf']
    
    def get_nome_completo(self, obj):
        return obj.usuario.get_full_name()
    get_nome_completo.short_description = 'Nome Completo'

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ['get_nome_completo', 'cargo', 'data_admissao', 'ativo']
    list_filter = ['ativo', 'cargo']
    search_fields = ['usuario__first_name', 'usuario__last_name']
    
    def get_nome_completo(self, obj):
        return obj.usuario.get_full_name()
    get_nome_completo.short_description = 'Nome Completo'
