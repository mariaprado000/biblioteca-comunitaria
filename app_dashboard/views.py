from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from app_livro.models import Livro
from app_leitor.models import Leitor
from app_emprestimo.models import Emprestimo
from django.utils import timezone

@login_required
def home(request):
    # Estatísticas para o dashboard
    total_livros = Livro.objects.count()
    total_leitores = Leitor.objects.filter(ativo=True).count()
    emprestimos_ativos = Emprestimo.objects.filter(data_devolucao__isnull=True).count()
    emprestimos_atrasados = Emprestimo.objects.filter(
        data_devolucao__isnull=True,
        data_devolucao_prevista__lt=timezone.now().date()
    ).count()
    
    context = {
        'total_livros': total_livros,
        'total_leitores': total_leitores,
        'emprestimos_ativos': emprestimos_ativos,
        'emprestimos_atrasados': emprestimos_atrasados,
    }
    
    return render(request, 'app_dashboard/home.html', context)
