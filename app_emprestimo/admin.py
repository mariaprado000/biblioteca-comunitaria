from django.contrib import admin
from .models import Emprestimo

@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('livro', 'leitor', 'emprestado_por', 'data_emprestimo', 'data_devolucao_prevista', 'data_devolucao', 'multa')
    list_filter = ('data_emprestimo', 'data_devolucao_prevista', 'data_devolucao')
    search_fields = ('livro__titulo', 'leitor__first_name', 'leitor__last_name')
    date_hierarchy = 'data_emprestimo'
