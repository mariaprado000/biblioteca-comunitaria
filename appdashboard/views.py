from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.utils import timezone

from accounts.models import Leitor, Funcionario
from appbiblioteca.models import Livro
from appemprestimos.models import Emprestimo

# Funções auxiliares
def is_funcionario(user):
    return user.groups.filter(name='Funcionários').exists() or user.is_superuser

def is_leitor(user):
    return user.groups.filter(name='Leitores').exists()

@login_required
def home(request):
    context = {}
    
    if is_funcionario(request.user):
        # Dashboard para funcionários
        context['total_livros'] = Livro.objects.count()
        context['livros_disponiveis'] = Livro.objects.filter(disponivel=True).count()
        context['total_leitores'] = Leitor.objects.filter(ativo=True).count()
        context['emprestimos_ativos'] = Emprestimo.objects.filter(data_devolucao__isnull=True).count()
        context['emprestimos_atrasados'] = Emprestimo.objects.filter(
            data_devolucao__isnull=True,
            data_devolucao_prevista__lt=timezone.now().date()
        ).count()
        
        # Livros mais emprestados
        context['livros_populares'] = Livro.objects.annotate(
            num_emprestimos=Count('emprestimo')
        ).order_by('-num_emprestimos')[:5]
        
    else:
        # Dashboard para leitores
        try:
            leitor = request.user.leitor
            context['meus_emprestimos'] = Emprestimo.objects.filter(
                leitor=leitor,
                data_devolucao__isnull=True
            )
            context['historico_emprestimos'] = Emprestimo.objects.filter(
                leitor=leitor
            ).order_by('-data_emprestimo')[:10]
            context['today'] = timezone.now().date()
        except:
            pass
    
    return render(request, 'appdashboard/home.html', context)

@login_required
@user_passes_test(is_funcionario)
def relatorio_livros_populares(request):
    livros = Livro.objects.annotate(
        num_emprestimos=Count('emprestimo')
    ).filter(num_emprestimos__gt=0).order_by('-num_emprestimos')
    
    # Calcular estatísticas
    total_emprestimos = sum(livro.num_emprestimos for livro in livros)
    
    context = {
        'livros': livros,
        'total_emprestimos': total_emprestimos
    }
    
    return render(request, 'appdashboard/relatorio_livros_populares.html', context)

