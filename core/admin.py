from django.contrib import admin
from .models import Livro, Leitor, Funcionario, Emprestimo, Categoria

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'ano', 'genero', 'categoria', 'disponivel']
    list_filter = ['disponivel', 'genero', 'categoria']
    search_fields = ['titulo', 'autor', 'isbn']

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

@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ['livro', 'leitor', 'data_emprestimo', 'data_devolucao_prevista', 'data_devolucao']
    list_filter = ['data_emprestimo', 'data_devolucao']
    search_fields = ['livro__titulo', 'leitor__usuario__first_name']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'criado_em']
    search_fields = ['nome']