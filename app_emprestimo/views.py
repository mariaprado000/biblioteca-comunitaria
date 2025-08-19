from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from .models import Emprestimo
from app_livro.models import Livro
from app_leitor.models import Leitor
from app_funcionario.models import Funcionario
from biblioteca.decorators import funcionario_or_leitor_required, funcionario_required

@login_required
@funcionario_or_leitor_required
def emprestimo_list(request):
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    
    emprestimos = Emprestimo.objects.select_related('livro', 'leitor__usuario', 'emprestado_por__usuario')
    
    if search:
        emprestimos = emprestimos.filter(
            livro__titulo__icontains=search
        ) | emprestimos.filter(
            leitor__usuario__first_name__icontains=search
        ) | emprestimos.filter(
            leitor__usuario__last_name__icontains=search
        )
    
    if status == 'ativo':
        emprestimos = emprestimos.filter(data_devolucao__isnull=True)
    elif status == 'atrasado':
        emprestimos = emprestimos.filter(
            data_devolucao__isnull=True,
            data_devolucao_prevista__lt=timezone.now().date()
        )
    elif status == 'devolvido':
        emprestimos = emprestimos.filter(data_devolucao__isnull=False)
    
    emprestimos = emprestimos.order_by('-data_emprestimo')
    
    context = {
        'emprestimos': emprestimos,
        'search': search,
        'status_filtro': status
    }
    return render(request, 'app_emprestimo/list.html', context)

@login_required
@funcionario_required
def emprestimo_create(request):
    if request.method == 'POST':
        try:
            livro_id = request.POST.get('livro')
            leitor_id = request.POST.get('leitor')
            dias_emprestimo = int(request.POST.get('dias_emprestimo', 14))
            
            livro = get_object_or_404(Livro, pk=livro_id)
            leitor = get_object_or_404(Leitor, pk=leitor_id)
            
            # Verificar se livro está disponível
            if not livro.disponivel:
                messages.error(request, 'Este livro não está disponível para empréstimo.')
                return redirect('app_emprestimo:criar')
            
            # Verificar se leitor está ativo
            if not leitor.ativo:
                messages.error(request, 'Este leitor está inativo.')
                return redirect('app_emprestimo:criar')
            
            # Obter funcionário atual
            funcionario = get_object_or_404(Funcionario, usuario=request.user)
            
            # Criar empréstimo
            data_devolucao_prevista = timezone.now().date() + timedelta(days=dias_emprestimo)
            
            emprestimo = Emprestimo(
                livro=livro,
                leitor=leitor,
                emprestado_por=funcionario,
                data_devolucao_prevista=data_devolucao_prevista
            )
            emprestimo.save()
            
            # Marcar livro como indisponível
            livro.disponivel = False
            livro.save()
            
            messages.success(request, 'Empréstimo realizado com sucesso!')
            return redirect('app_emprestimo:listar')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar empréstimo: {e}')
    
    livros_disponiveis = Livro.objects.filter(disponivel=True).order_by('titulo')
    leitores_ativos = Leitor.objects.filter(ativo=True).order_by('usuario__first_name')
    
    context = {
        'livros': livros_disponiveis,
        'leitores': leitores_ativos
    }
    return render(request, 'app_emprestimo/form.html', context)

@login_required
@funcionario_required
def emprestimo_devolver(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    
    if emprestimo.data_devolucao:
        messages.warning(request, 'Este empréstimo já foi devolvido.')
        return redirect('app_emprestimo:listar')
    
    if request.method == 'POST':
        try:
            # Marcar data de devolução
            emprestimo.data_devolucao = timezone.now().date()
            
            # Calcular multa se houver atraso
            emprestimo.multa = emprestimo.calcular_multa()
            emprestimo.save()
            
            # Marcar livro como disponível
            emprestimo.livro.disponivel = True
            emprestimo.livro.save()
            
            if emprestimo.multa > 0:
                messages.warning(request, f'Livro devolvido com multa de R$ {emprestimo.multa:.2f}')
            else:
                messages.success(request, 'Livro devolvido com sucesso!')
                
            return redirect('app_emprestimo:listar')
            
        except Exception as e:
            messages.error(request, f'Erro ao devolver livro: {e}')
    
    # Calcular multa atual (se houver)
    multa_atual = emprestimo.calcular_multa()
    
    context = {
        'object': emprestimo,
        'multa_atual': multa_atual
    }
    return render(request, 'app_emprestimo/devolver.html', context)

@login_required
@funcionario_required
def emprestimo_renovar(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    
    if emprestimo.data_devolucao:
        messages.warning(request, 'Este empréstimo já foi devolvido.')
        return redirect('app_emprestimo:listar')
    
    if not emprestimo.pode_renovar():
        messages.error(request, 'Este empréstimo não pode ser renovado (atrasado ou limite de renovações atingido).')
        return redirect('app_emprestimo:listar')
    
    if request.method == 'POST':
        try:
            dias_renovacao = int(request.POST.get('dias_renovacao', 14))
            
            # Renovar empréstimo
            emprestimo.data_devolucao_prevista += timedelta(days=dias_renovacao)
            emprestimo.renovacao += 1
            emprestimo.save()
            
            messages.success(request, f'Empréstimo renovado por {dias_renovacao} dias!')
            return redirect('app_emprestimo:listar')
            
        except Exception as e:
            messages.error(request, f'Erro ao renovar empréstimo: {e}')
    
    context = {
        'object': emprestimo
    }
    return render(request, 'app_emprestimo/renovar.html', context)
