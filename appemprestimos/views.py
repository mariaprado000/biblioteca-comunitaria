from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from decimal import Decimal
from .models import Emprestimo
from .forms import EmprestimoForm

from accounts.models import Funcionario
from appbiblioteca.models import Livro

# Função auxiliar
def is_funcionario(user):
    return user.groups.filter(name='Funcionários').exists() or user.is_superuser

def is_leitor(user):
    return user.groups.filter(name='Leitores').exists()

# CRUD EMPRÉSTIMOS
@login_required
def emprestimo_list(request):
    emprestimos_atrasados = 0
    
    if is_funcionario(request.user):
        emprestimos = Emprestimo.objects.all()
        # Contar empréstimos atrasados
        emprestimos_atrasados = Emprestimo.objects.filter(
            data_devolucao__isnull=True,
            data_devolucao_prevista__lt=timezone.now().date()
        ).count()
    else:
        try:
            leitor = request.user.leitor
            emprestimos = Emprestimo.objects.filter(leitor=leitor)
        except:
            emprestimos = Emprestimo.objects.none()
    
    # Adicionar informações extras para o template
    for emprestimo in emprestimos:
        emprestimo.multa_atual = emprestimo.calcular_multa()
        emprestimo.atrasado = emprestimo.esta_atrasado()
    
    return render(request, 'appemprestimos/emprestimo_list.html', {
        'emprestimos': emprestimos,
        'emprestimos_atrasados': emprestimos_atrasados,
        'today': timezone.now().date()
    })

@login_required
@user_passes_test(is_funcionario)
@transaction.atomic
def emprestimo_create(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo = form.save(commit=False)
            
            # Adicionar funcionário
            try:
                funcionario = Funcionario.objects.get(usuario=request.user)
                emprestimo.funcionario = funcionario
            except Funcionario.DoesNotExist:
                pass
            
            # Marcar livro como indisponível
            livro = emprestimo.livro
            livro.disponivel = False
            livro.save()
            
            emprestimo.save()
            messages.success(request, 'Empréstimo realizado com sucesso!')
            return redirect('emprestimo_list')
    else:
        form = EmprestimoForm()
    
    return render(request, 'appemprestimos/emprestimo_form.html', {'form': form})

@login_required
@user_passes_test(is_funcionario)
@transaction.atomic
def emprestimo_update(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    livro_anterior = emprestimo.livro
    
    if request.method == 'POST':
        form = EmprestimoForm(request.POST, instance=emprestimo)
        if form.is_valid():
            emprestimo = form.save()
            
            # Se mudou o livro, atualizar disponibilidade
            if livro_anterior != emprestimo.livro:
                livro_anterior.disponivel = True
                livro_anterior.save()
                emprestimo.livro.disponivel = False
                emprestimo.livro.save()
            
            messages.success(request, 'Empréstimo atualizado com sucesso!')
            return redirect('emprestimo_list')
    else:
        form = EmprestimoForm(instance=emprestimo)
    
    return render(request, 'appemprestimos/emprestimo_form.html', {'form': form})

@login_required
@user_passes_test(is_funcionario)
@transaction.atomic
def emprestimo_delete(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    
    if request.method == 'POST':
        # Marcar livro como disponível novamente
        emprestimo.livro.disponivel = True
        emprestimo.livro.save()
        emprestimo.delete()
        messages.success(request, 'Empréstimo excluído com sucesso!')
        return redirect('emprestimo_list')
    
    return render(request, 'appemprestimos/emprestimo_confirm_delete.html', {'emprestimo': emprestimo})

@login_required
@user_passes_test(is_funcionario)
@transaction.atomic
def emprestimo_devolver(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    
    if request.method == 'POST':
        emprestimo.data_devolucao = timezone.now().date()
        emprestimo.multa = emprestimo.calcular_multa()
        emprestimo.save()
        
        # Marcar livro como disponível
        emprestimo.livro.disponivel = True
        emprestimo.livro.save()
        
        if emprestimo.multa > 0:
            messages.warning(request, f'Devolução realizada com multa de R$ {emprestimo.multa}')
        else:
            messages.success(request, 'Devolução realizada com sucesso!')
        
        return redirect('emprestimo_list')
    
    # Calcular multa para exibir
    multa_prevista = emprestimo.calcular_multa()
    
    return render(request, 'appemprestimos/emprestimo_devolver.html', {
        'emprestimo': emprestimo,
        'multa_prevista': multa_prevista
    })

@login_required
@transaction.atomic
def emprestimo_renovar(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    
    # Verificar permissão
    if not is_funcionario(request.user):
        try:
            leitor = request.user.leitor
            if emprestimo.leitor != leitor:
                messages.error(request, 'Você só pode renovar seus próprios empréstimos!')
                return redirect('emprestimo_list')
        except:
            messages.error(request, 'Acesso negado!')
            return redirect('home')
    
    if request.method == 'POST':
        if not emprestimo.pode_renovar():
            messages.error(request, 'Este empréstimo não pode ser renovado!')
            return redirect('emprestimo_list')
        
        # Renovar por mais 14 dias
        nova_data = emprestimo.data_devolucao_prevista + timedelta(days=14)
        
        # Verificar se não ultrapassa 60 dias totais
        dias_totais = (nova_data - emprestimo.data_emprestimo.date()).days
        if dias_totais > 60:
            messages.error(request, 'O empréstimo não pode exceder 60 dias no total!')
            return redirect('emprestimo_list')
        
        emprestimo.data_devolucao_prevista = nova_data
        emprestimo.renovacoes += 1
        emprestimo.save()
        
        messages.success(request, f'Empréstimo renovado até {nova_data.strftime("%d/%m/%Y")}!')
        return redirect('emprestimo_list')
    
    return render(request, 'appemprestimos/emprestimo_renovar.html', {
        'emprestimo': emprestimo,
        'pode_renovar': emprestimo.pode_renovar()
    })

# Relatórios
@login_required
@user_passes_test(is_funcionario)
def relatorio_atrasos(request):
    emprestimos_atraso = Emprestimo.objects.filter(
        data_devolucao__isnull=True,
        data_devolucao_prevista__lt=timezone.now().date()
    ).select_related('livro', 'leitor__usuario')
    
    # Calcular multas
    for emprestimo in emprestimos_atraso:
        emprestimo.multa_atual = emprestimo.calcular_multa()
        emprestimo.dias_atraso = (timezone.now().date() - emprestimo.data_devolucao_prevista).days
    
    return render(request, 'appemprestimos/relatorio_atrasos.html', {
        'emprestimos': emprestimos_atraso
    })

