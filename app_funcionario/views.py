from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Funcionario

def is_funcionario(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_funcionario)
def funcionario_list(request):
    search = request.GET.get('search', '')
    
    funcionarios = Funcionario.objects.select_related('usuario')
    
    if search:
        funcionarios = funcionarios.filter(
            usuario__first_name__icontains=search
        ) | funcionarios.filter(
            usuario__last_name__icontains=search
        ) | funcionarios.filter(
            cargo__icontains=search
        )
    
    funcionarios = funcionarios.order_by('usuario__first_name')
    
    context = {
        'funcionarios': funcionarios,
        'search': search
    }
    return render(request, 'app_funcionario/list.html', context)

@login_required
@user_passes_test(is_funcionario)
def funcionario_create(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Criar usuário
                user = User.objects.create_user(
                    username=request.POST.get('username'),
                    email=request.POST.get('email', ''),
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    password=request.POST.get('password'),
                    is_staff=True  # Funcionários são staff
                )
                
                # Criar funcionário
                funcionario = Funcionario(
                    usuario=user,
                    cargo=request.POST.get('cargo'),
                    salario=float(request.POST.get('salario')),
                    data_admissao=request.POST.get('data_admissao')
                )
                funcionario.full_clean()
                funcionario.save()
                
                messages.success(request, 'Funcionário criado com sucesso!')
                return redirect('app_funcionario:listar')
        except ValidationError as e:
            messages.error(request, f'Erro de validação: {e}')
        except Exception as e:
            messages.error(request, f'Erro ao criar funcionário: {e}')
    
    return render(request, 'app_funcionario/form.html')

@login_required
@user_passes_test(is_funcionario)
def funcionario_update(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Atualizar usuário
                user = funcionario.usuario
                user.username = request.POST.get('username')
                user.email = request.POST.get('email', '')
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                
                # Atualizar senha se fornecida
                new_password = request.POST.get('password')
                if new_password:
                    user.set_password(new_password)
                
                user.save()
                
                # Atualizar funcionário
                funcionario.cargo = request.POST.get('cargo')
                funcionario.salario = float(request.POST.get('salario'))
                funcionario.data_admissao = request.POST.get('data_admissao')
                funcionario.ativo = request.POST.get('ativo') == 'on'
                
                funcionario.full_clean()
                funcionario.save()
                
                messages.success(request, 'Funcionário atualizado com sucesso!')
                return redirect('app_funcionario:listar')
        except ValidationError as e:
            messages.error(request, f'Erro de validação: {e}')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar funcionário: {e}')
    
    return render(request, 'app_funcionario/form.html', {'object': funcionario})

@login_required
@user_passes_test(is_funcionario)
def funcionario_delete(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        # Desativar ao invés de deletar
        funcionario.ativo = False
        funcionario.save()
        messages.success(request, 'Funcionário desativado com sucesso!')
        return redirect('app_funcionario:listar')
    return render(request, 'app_funcionario/confirm_delete.html', {'object': funcionario})
