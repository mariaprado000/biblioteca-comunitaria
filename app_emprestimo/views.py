from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import Emprestimo
from .forms import EmprestimoForm, RenovacaoForm, DevolucaoForm
from app_livro.models import Livro
from app_leitor.models import Leitor
from app_funcionario.models import Funcionario
from biblioteca.decorators import funcionario_or_leitor_required, funcionario_required

def calcular_multa(emprestimo):
    """Calcula a multa baseada nos dias de atraso"""
    if not emprestimo.data_devolucao and emprestimo.data_devolucao_prevista < timezone.now().date():
        dias_atraso = (timezone.now().date() - emprestimo.data_devolucao_prevista).days
        return Decimal(str(dias_atraso * 2.00))
    elif emprestimo.data_devolucao and emprestimo.data_devolucao > emprestimo.data_devolucao_prevista:
        dias_atraso = (emprestimo.data_devolucao - emprestimo.data_devolucao_prevista).days
        return Decimal(str(dias_atraso * 2.00))
    return Decimal('0.00')

@login_required
@funcionario_or_leitor_required
def emprestimo_list(request):
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    
    emprestimos = Emprestimo.objects.select_related('livro', 'leitor', 'emprestado_por')
    
    if search:
        emprestimos = emprestimos.filter(
            livro__titulo__icontains=search
        ) | emprestimos.filter(
            leitor__first_name__icontains=search
        ) | emprestimos.filter(
            leitor__last_name__icontains=search
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
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            try:
                # Obter funcionário atual
                funcionario = Funcionario.objects.get(pk=request.user.pk)
                
                # Criar empréstimo
                dias_emprestimo = form.cleaned_data['dias_emprestimo']
                data_devolucao_prevista = timezone.now().date() + timedelta(days=dias_emprestimo)
                
                emprestimo = form.save(commit=False)
                emprestimo.emprestado_por = funcionario
                emprestimo.data_devolucao_prevista = data_devolucao_prevista
                emprestimo.save()
                
                # Marcar livro como indisponível
                emprestimo.livro.disponivel = False
                emprestimo.livro.save()
                
                messages.success(request, 'Empréstimo realizado com sucesso!')
                return redirect('app_emprestimo:listar')
                
            except Exception as e:
                messages.error(request, f'Erro ao criar empréstimo: {e}')
    else:
        form = EmprestimoForm()
    
    context = {
        'form': form
    }
    return render(request, 'app_emprestimo/form.html', context)

@login_required
@funcionario_required
def emprestimo_devolver(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    
    if request.method == 'POST':
        form = DevolucaoForm(emprestimo=emprestimo, data=request.POST)
        if form.is_valid():
            try:
                # Marcar data de devolução
                emprestimo.data_devolucao = timezone.now().date()
                
                # Calcular multa se houver atraso
                emprestimo.multa = calcular_multa(emprestimo)
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
    else:
        form = DevolucaoForm(emprestimo=emprestimo)
    
    # Calcular multa atual (se houver)
    multa_atual = calcular_multa(emprestimo)
    
    context = {
        'form': form,
        'object': emprestimo,
        'multa_atual': multa_atual
    }
    return render(request, 'app_emprestimo/devolver.html', context)

@login_required
@funcionario_required
def emprestimo_renovar(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    
    if request.method == 'POST':
        form = RenovacaoForm(emprestimo=emprestimo, data=request.POST)
        if form.is_valid():
            try:
                dias_renovacao = form.cleaned_data['dias_renovacao']
                funcionario = Funcionario.objects.get(pk=request.user.pk)
                
                # Criar novo empréstimo (renovação) vinculado ao atual
                novo_emprestimo = Emprestimo(
                    livro=emprestimo.livro,
                    leitor=emprestimo.leitor,
                    emprestado_por=funcionario,
                    data_devolucao_prevista=emprestimo.data_devolucao_prevista + timedelta(days=dias_renovacao),
                    renovacao=emprestimo
                )
                novo_emprestimo.save()
                
                # Marcar empréstimo atual como devolvido
                emprestimo.data_devolucao = timezone.now().date()
                emprestimo.save()
                
                messages.success(request, f'Empréstimo renovado por {dias_renovacao} dias!')
                return redirect('app_emprestimo:listar')
                
            except Exception as e:
                messages.error(request, f'Erro ao renovar empréstimo: {e}')
    else:
        form = RenovacaoForm(emprestimo=emprestimo)
    
    context = {
        'form': form,
        'object': emprestimo
    }
    return render(request, 'app_emprestimo/renovar.html', context)
