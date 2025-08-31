from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from app_livro.models import Livro
from app_leitor.models import Leitor
from app_emprestimo.models import Emprestimo
from django.utils import timezone
from biblioteca.decorators import funcionario_or_leitor_required

@login_required
@funcionario_or_leitor_required
def home(request):
    # Verificar se é funcionário
    is_funcionario = request.user.groups.filter(name='Funcionarios').exists()
    
    context = {}
    
    if is_funcionario:
        # Dados administrativos para funcionários
        context.update({
            'total_livros': Livro.objects.count(),
            'total_leitores': Leitor.objects.filter(ativo=True).count(),
            'emprestimos_ativos': Emprestimo.objects.filter(data_devolucao__isnull=True).count(),
            'emprestimos_atrasados': Emprestimo.objects.filter(
                data_devolucao__isnull=True,
                data_devolucao_prevista__lt=timezone.now().date()
            ).count(),
        })
    else:
        # Dados limitados para leitores
        try:
            leitor = Leitor.objects.get(pk=request.user.pk)
            meus_emprestimos = Emprestimo.objects.filter(
                leitor=leitor,
                data_devolucao__isnull=True
            )
            context.update({
                'total_livros': Livro.objects.filter(disponivel=True).count(),  # Apenas disponíveis
                'meus_emprestimos_ativos': meus_emprestimos.count(),
                'meus_emprestimos_atrasados': meus_emprestimos.filter(
                    data_devolucao_prevista__lt=timezone.now().date()
                ).count(),
                'meus_emprestimos': meus_emprestimos[:3],  # Últimos 3 empréstimos
            })
        except Leitor.DoesNotExist:
            context.update({
                'total_livros': Livro.objects.filter(disponivel=True).count(),
                'meus_emprestimos_ativos': 0,
                'meus_emprestimos_atrasados': 0,
                'meus_emprestimos': [],
            })
    
    return render(request, 'app_dashboard/home.html', context)
