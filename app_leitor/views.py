from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Leitor
from .forms import LeitorForm
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
        form = LeitorForm(request.POST)
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
                    
                    # Adicionar ao grupo Leitores
                    leitores_group, created = Group.objects.get_or_create(name='Leitores')
                    user.groups.add(leitores_group)
                    
                    # Criar leitor
                    leitor = form.save(commit=False)
                    leitor.usuario = user
                    leitor.save()
                    
                    messages.success(request, 'Leitor criado com sucesso!')
                    return redirect('app_leitor:listar')
            except Exception as e:
                messages.error(request, f'Erro ao criar leitor: {e}')
        else:
            if not username:
                messages.error(request, 'Nome de usuário é obrigatório')
            if not password:
                messages.error(request, 'Senha é obrigatória')
    else:
        form = LeitorForm()
    
    return render(request, 'app_leitor/form.html', {'form': form})

@login_required
@funcionario_required
def leitor_update(request, pk):
    leitor = get_object_or_404(Leitor, pk=pk)
    
    if request.method == 'POST':
        form = LeitorForm(request.POST, instance=leitor)
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Atualizar usuário
                    user = leitor.usuario
                    if username:
                        user.username = username
                    user.email = form.cleaned_data['email']
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    
                    # Atualizar senha se fornecida
                    if password:
                        user.set_password(password)
                    
                    user.save()
                    
                    # Atualizar leitor
                    leitor = form.save(commit=False)
                    leitor.ativo = request.POST.get('ativo') == 'on'
                    leitor.save()
                    
                    messages.success(request, 'Leitor atualizado com sucesso!')
                    return redirect('app_leitor:listar')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar leitor: {e}')
    else:
        form = LeitorForm(instance=leitor, initial={
            'first_name': leitor.usuario.first_name,
            'last_name': leitor.usuario.last_name,
            'email': leitor.usuario.email,
        })
    
    return render(request, 'app_leitor/form.html', {
        'form': form, 
        'object': leitor
    })

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
