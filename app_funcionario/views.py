from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Funcionario
from .forms import FuncionarioForm
from biblioteca.decorators import funcionario_required

@login_required
@funcionario_required
def funcionario_list(request):
    search = request.GET.get('search', '')
    
    funcionarios = Funcionario.objects.all()
    
    if search:
        funcionarios = funcionarios.filter(
            first_name__icontains=search
        ) | funcionarios.filter(
            last_name__icontains=search
        ) | funcionarios.filter(
            cargo__icontains=search
        )
    
    funcionarios = funcionarios.order_by('first_name')
    
    context = {
        'funcionarios': funcionarios,
        'search': search
    }
    return render(request, 'app_funcionario/list.html', context)

@login_required
@funcionario_required
def funcionario_create(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if form.is_valid() and username and password:
            try:
                with transaction.atomic():
                    # Criar funcionário (que herda de User)
                    funcionario = form.save(commit=False)
                    funcionario.username = username
                    funcionario.set_password(password)
                    funcionario.save()
                    
                    # Adicionar ao grupo Funcionarios
                    funcionarios_group, created = Group.objects.get_or_create(name='Funcionarios')
                    funcionario.groups.add(funcionarios_group)
                    
                    messages.success(request, 'Funcionário criado com sucesso!')
                    return redirect('app_funcionario:listar')
            except Exception as e:
                messages.error(request, f'Erro ao criar funcionário: {e}')
        else:
            if not username:
                messages.error(request, 'Nome de usuário é obrigatório')
            if not password:
                messages.error(request, 'Senha é obrigatória')
    else:
        form = FuncionarioForm()
    
    return render(request, 'app_funcionario/form.html', {'form': form})

@login_required
@funcionario_required
def funcionario_update(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Atualizar funcionário (que herda de User)
                    funcionario = form.save(commit=False)
                    if username:
                        funcionario.username = username
                    
                    # Atualizar senha se fornecida
                    if password:
                        funcionario.set_password(password)
                    
                    funcionario.ativo = request.POST.get('ativo') == 'on'
                    funcionario.save()
                    
                    messages.success(request, 'Funcionário atualizado com sucesso!')
                    return redirect('app_funcionario:listar')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar funcionário: {e}')
    else:
        form = FuncionarioForm(instance=funcionario)
    
    return render(request, 'app_funcionario/form.html', {
        'form': form, 
        'object': funcionario
    })

@login_required
@funcionario_required
def funcionario_delete(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        # Desativar ao invés de deletar
        funcionario.ativo = False
        funcionario.save()
        messages.success(request, 'Funcionário desativado com sucesso!')
        return redirect('app_funcionario:listar')
    return render(request, 'app_funcionario/confirm_delete.html', {'object': funcionario})
