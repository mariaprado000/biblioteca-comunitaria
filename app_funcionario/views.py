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
@funcionario_required
def funcionario_create(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if form.is_valid() and username and password:
            try:
                with transaction.atomic():
                    # Criar usuário
                    user = User.objects.create_user(
                        username=username,
                        email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        password=password
                    )
                    
                    # Adicionar ao grupo Funcionarios
                    funcionarios_group, created = Group.objects.get_or_create(name='Funcionarios')
                    user.groups.add(funcionarios_group)
                    
                    # Criar funcionário
                    funcionario = form.save(commit=False)
                    funcionario.usuario = user
                    funcionario.save()
                    
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
                    # Atualizar usuário
                    user = funcionario.usuario
                    if username:
                        user.username = username
                    user.email = form.cleaned_data['email']
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    
                    # Atualizar senha se fornecida
                    if password:
                        user.set_password(password)
                    
                    user.save()
                    
                    # Atualizar funcionário
                    funcionario = form.save(commit=False)
                    funcionario.ativo = request.POST.get('ativo') == 'on'
                    funcionario.save()
                    
                    messages.success(request, 'Funcionário atualizado com sucesso!')
                    return redirect('app_funcionario:listar')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar funcionário: {e}')
    else:
        form = FuncionarioForm(instance=funcionario, initial={
            'first_name': funcionario.usuario.first_name,
            'last_name': funcionario.usuario.last_name,
            'email': funcionario.usuario.email,
        })
    
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
