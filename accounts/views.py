from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .models import Leitor, Funcionario
from .forms import LeitorForm, FuncionarioForm, RegistroForm

# Funções auxiliares para verificar grupos
def is_funcionario(user):
    return user.groups.filter(name='Funcionários').exists() or user.is_superuser

def is_leitor(user):
    return user.groups.filter(name='Leitores').exists()

# View Registro
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Adicionar usuário ao grupo padrão
            try:
                grupo_leitores = Group.objects.get(name='Leitores')
                user.groups.add(grupo_leitores)
            except Group.DoesNotExist:
                pass
            login(request, user)
            messages.success(request, 'Registro realizado com sucesso! Complete seu cadastro como leitor.')
            return redirect('leitor_create_self')
    else:
        form = RegistroForm()
    return render(request, 'accounts/registro.html', {'form': form})

# CRUD LEITORES
@login_required
@user_passes_test(is_funcionario)
def leitor_list(request):
    from django.db.models import Q
    query = request.GET.get('q')
    if query:
        leitores = Leitor.objects.filter(
            Q(usuario__first_name__icontains=query) |
            Q(usuario__last_name__icontains=query) |
            Q(cpf__icontains=query)
        ).order_by('usuario__first_name')
    else:
        leitores = Leitor.objects.all().order_by('usuario__first_name')
    return render(request, 'accounts/leitor_list.html', {'leitores': leitores, 'query': query})

@login_required
def leitor_create_self(request):
    """Permite que um usuário recém-registrado crie seu próprio perfil de leitor"""
    if hasattr(request.user, 'leitor'):
        messages.info(request, 'Você já possui um cadastro de leitor.')
        return redirect('home')
    
    if request.method == 'POST':
        form = LeitorForm(request.POST)
        if form.is_valid():
            leitor = form.save(commit=False)
            leitor.usuario = request.user
            # Atualizar dados do usuário
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            leitor.save()
            messages.success(request, 'Cadastro de leitor concluído com sucesso!')
            return redirect('home')
    else:
        form = LeitorForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
    return render(request, 'accounts/leitor_form.html', {'form': form, 'self_register': True})

@login_required
@user_passes_test(is_funcionario)
def leitor_create(request):
    if request.method == 'POST':
        form = LeitorForm(request.POST)
        if form.is_valid():
            # Criar usuário
            username = form.cleaned_data['cpf']
            user = User.objects.create_user(
                username=username,
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password='senha123'
            )
            # Adicionar ao grupo Leitores
            try:
                grupo_leitores = Group.objects.get(name='Leitores')
                user.groups.add(grupo_leitores)
            except Group.DoesNotExist:
                pass
            # Criar leitor
            leitor = form.save(commit=False)
            leitor.usuario = user
            leitor.save()
            messages.success(request, 'Leitor cadastrado com sucesso! Senha padrão: senha123')
            return redirect('leitor_list')
    else:
        form = LeitorForm()
    return render(request, 'accounts/leitor_form.html', {'form': form})

@login_required
@user_passes_test(is_funcionario)
def leitor_update(request, pk):
    leitor = get_object_or_404(Leitor, pk=pk)
    if request.method == 'POST':
        form = LeitorForm(request.POST, instance=leitor)
        if form.is_valid():
            # Atualizar dados do usuário
            leitor.usuario.first_name = form.cleaned_data['first_name']
            leitor.usuario.last_name = form.cleaned_data['last_name']
            leitor.usuario.email = form.cleaned_data['email']
            leitor.usuario.save()
            form.save()
            messages.success(request, 'Leitor atualizado com sucesso!')
            return redirect('leitor_list')
    else:
        form = LeitorForm(instance=leitor, initial={
            'first_name': leitor.usuario.first_name,
            'last_name': leitor.usuario.last_name,
            'email': leitor.usuario.email,
        })
    return render(request, 'accounts/leitor_form.html', {'form': form})

@login_required
@user_passes_test(is_funcionario)
def leitor_delete(request, pk):
    leitor = get_object_or_404(Leitor, pk=pk)
    if request.method == 'POST':
        leitor.usuario.delete()
        messages.success(request, 'Leitor excluído com sucesso!')
        return redirect('leitor_list')
    return render(request, 'accounts/leitor_confirm_delete.html', {'leitor': leitor})

# CRUD FUNCIONÁRIOS
@login_required
@user_passes_test(is_funcionario)
def funcionario_list(request):
    funcionarios = Funcionario.objects.all().order_by('usuario__first_name')
    return render(request, 'accounts/funcionario_list.html', {'funcionarios': funcionarios})

@login_required
@user_passes_test(is_funcionario)
def funcionario_create(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            # Criar usuário
            username = f"func_{form.cleaned_data['email'].split('@')[0]}"
            user = User.objects.create_user(
                username=username,
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password='senha123'
            )
            user.is_staff = True
            user.save()
            # Adicionar ao grupo Funcionários
            try:
                grupo_funcionarios = Group.objects.get(name='Funcionários')
                user.groups.add(grupo_funcionarios)
            except Group.DoesNotExist:
                pass
            # Criar funcionário
            funcionario = form.save(commit=False)
            funcionario.usuario = user
            funcionario.save()
            messages.success(request, 'Funcionário cadastrado com sucesso! Senha padrão: senha123')
            return redirect('funcionario_list')
    else:
        form = FuncionarioForm()
    return render(request, 'accounts/funcionario_form.html', {'form': form})

@login_required
@user_passes_test(is_funcionario)
def funcionario_update(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            # Atualizar dados do usuário
            funcionario.usuario.first_name = form.cleaned_data['first_name']
            funcionario.usuario.last_name = form.cleaned_data['last_name']
            funcionario.usuario.email = form.cleaned_data['email']
            funcionario.usuario.save()
            form.save()
            messages.success(request, 'Funcionário atualizado com sucesso!')
            return redirect('funcionario_list')
    else:
        form = FuncionarioForm(instance=funcionario, initial={
            'first_name': funcionario.usuario.first_name,
            'last_name': funcionario.usuario.last_name,
            'email': funcionario.usuario.email,
        })
    return render(request, 'accounts/funcionario_form.html', {'form': form})

@login_required
@user_passes_test(is_funcionario)
def funcionario_delete(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        funcionario.usuario.delete()
        messages.success(request, 'Funcionário excluído com sucesso!')
        return redirect('funcionario_list')
    return render(request, 'accounts/funcionario_confirm_delete.html', {'funcionario': funcionario})
