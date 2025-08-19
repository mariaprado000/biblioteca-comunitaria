from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Leitor
from biblioteca.decorators import funcionario_required

@login_required
@funcionario_required
def leitor_list(request):
    search = request.GET.get('search', '')
    
    leitores = Leitor.objects.select_related('usuario')
    
    if search:
        leitores = leitores.filter(
            usuario__first_name__icontains=search
        ) | leitores.filter(
            usuario__last_name__icontains=search
        ) | leitores.filter(
            cpf__icontains=search
        )
    
    leitores = leitores.order_by('usuario__first_name')
    
    context = {
        'leitores': leitores,
        'search': search
    }
    return render(request, 'app_leitor/list.html', context)

@login_required
@funcionario_required
def leitor_create(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Criar usuário
                user = User.objects.create_user(
                    username=request.POST.get('username'),
                    email=request.POST.get('email', ''),
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    password=request.POST.get('password')
                )
                
                # Criar leitor
                leitor = Leitor(
                    usuario=user,
                    cpf=request.POST.get('cpf'),
                    telefone=request.POST.get('telefone'),
                    endereco=request.POST.get('endereco'),
                    data_nascimento=request.POST.get('data_nascimento')
                )
                leitor.full_clean()
                leitor.save()
                
                messages.success(request, 'Leitor criado com sucesso!')
                return redirect('app_leitor:listar')
        except ValidationError as e:
            messages.error(request, f'Erro de validação: {e}')
        except Exception as e:
            messages.error(request, f'Erro ao criar leitor: {e}')
    
    return render(request, 'app_leitor/form.html')

@login_required
@funcionario_required
def leitor_update(request, pk):
    leitor = get_object_or_404(Leitor, pk=pk)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Atualizar usuário
                user = leitor.usuario
                user.username = request.POST.get('username')
                user.email = request.POST.get('email', '')
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                
                # Atualizar senha se fornecida
                new_password = request.POST.get('password')
                if new_password:
                    user.set_password(new_password)
                
                user.save()
                
                # Atualizar leitor
                leitor.cpf = request.POST.get('cpf')
                leitor.telefone = request.POST.get('telefone')
                leitor.endereco = request.POST.get('endereco')
                leitor.data_nascimento = request.POST.get('data_nascimento')
                leitor.ativo = request.POST.get('ativo') == 'on'
                
                leitor.full_clean()
                leitor.save()
                
                messages.success(request, 'Leitor atualizado com sucesso!')
                return redirect('app_leitor:listar')
        except ValidationError as e:
            messages.error(request, f'Erro de validação: {e}')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar leitor: {e}')
    
    return render(request, 'app_leitor/form.html', {'object': leitor})

@login_required
@funcionario_required
def leitor_delete(request, pk):
    leitor = get_object_or_404(Leitor, pk=pk)
    if request.method == 'POST':
        # Desativar ao invés de deletar
        leitor.ativo = False
        leitor.save()
        messages.success(request, 'Leitor desativado com sucesso!')
        return redirect('app_leitor:listar')
    return render(request, 'app_leitor/confirm_delete.html', {'object': leitor})
