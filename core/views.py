from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .models import Livro, Leitor, Funcionario, Emprestimo, Categoria
from .forms import LivroForm, LeitorForm, FuncionarioForm, EmprestimoForm, CategoriaForm, RegistroForm

# View Home
@login_required
def home(request):
    return render(request, 'core/home.html')

# View Registro
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Adicionar usuário ao grupo padrão se existir
            try:
                grupo_leitores = Group.objects.get(name='Leitores')
                user.groups.add(grupo_leitores)
            except Group.DoesNotExist:
                pass
            login(request, user)
            messages.success(request, 'Registro realizado com sucesso!')
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'core/registro.html', {'form': form})

# CRUD LIVROS
@login_required
def livro_list(request):
    livros = Livro.objects.all().order_by('titulo')
    return render(request, 'core/livro_list.html', {'livros': livros})

@login_required
def livro_create(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro cadastrado com sucesso!')
            return redirect('livro_list')
    else:
        form = LivroForm()
    return render(request, 'core/livro_form.html', {'form': form})

@login_required
def livro_update(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro atualizado com sucesso!')
            return redirect('livro_list')
    else:
        form = LivroForm(instance=livro)
    return render(request, 'core/livro_form.html', {'form': form})

@login_required
def livro_delete(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        livro.delete()
        messages.success(request, 'Livro excluído com sucesso!')
        return redirect('livro_list')
    return render(request, 'core/livro_confirm_delete.html', {'livro': livro})

# CRUD LEITORES
@login_required
def leitor_list(request):
    leitores = Leitor.objects.all().order_by('usuario__first_name')
    return render(request, 'core/leitor_list.html', {'leitores': leitores})

@login_required
def leitor_create(request):
    if request.method == 'POST':
        form = LeitorForm(request.POST)
        if form.is_valid():
            # Criar usuário
            username = form.cleaned_data['cpf']  # Usar CPF como username
            user = User.objects.create_user(
                username=username,
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password='senha123'  # Senha padrão
            )
            # Criar leitor
            leitor = form.save(commit=False)
            leitor.usuario = user
            leitor.save()
            messages.success(request, 'Leitor cadastrado com sucesso! Senha padrão: senha123')
            return redirect('leitor_list')
    else:
        form = LeitorForm()
    return render(request, 'core/leitor_form.html', {'form': form})

@login_required
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
    return render(request, 'core/leitor_form.html', {'form': form})

@login_required
def leitor_delete(request, pk):
    leitor = get_object_or_404(Leitor, pk=pk)
    if request.method == 'POST':
        leitor.usuario.delete()  # Deletar usuário também deleta o leitor
        messages.success(request, 'Leitor excluído com sucesso!')
        return redirect('leitor_list')
    return render(request, 'core/leitor_confirm_delete.html', {'leitor': leitor})

# CRUD FUNCIONÁRIOS
@login_required
def funcionario_list(request):
    funcionarios = Funcionario.objects.all().order_by('usuario__first_name')
    return render(request, 'core/funcionario_list.html', {'funcionarios': funcionarios})

@login_required
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
                password='senha123'  # Senha padrão
            )
            user.is_staff = True  # Funcionário tem acesso ao admin
            user.save()
            # Criar funcionário
            funcionario = form.save(commit=False)
            funcionario.usuario = user
            funcionario.save()
            messages.success(request, 'Funcionário cadastrado com sucesso! Senha padrão: senha123')
            return redirect('funcionario_list')
    else:
        form = FuncionarioForm()
    return render(request, 'core/funcionario_form.html', {'form': form})

@login_required
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
    return render(request, 'core/funcionario_form.html', {'form': form})

@login_required
def funcionario_delete(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        funcionario.usuario.delete()  # Deletar usuário também deleta o funcionário
        messages.success(request, 'Funcionário excluído com sucesso!')
        return redirect('funcionario_list')
    return render(request, 'core/funcionario_confirm_delete.html', {'funcionario': funcionario})

# CRUD EMPRÉSTIMOS
@login_required
def emprestimo_list(request):
    emprestimos = Emprestimo.objects.all().order_by('-data_emprestimo')
    return render(request, 'core/emprestimo_list.html', {'emprestimos': emprestimos})

@login_required
def emprestimo_create(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo = form.save(commit=False)
            # Verificar se o usuário é funcionário
            try:
                funcionario = Funcionario.objects.get(usuario=request.user)
                emprestimo.funcionario = funcionario
            except Funcionario.DoesNotExist:
                pass
            # Marcar livro como indisponível
            emprestimo.livro.disponivel = False
            emprestimo.livro.save()
            emprestimo.save()
            messages.success(request, 'Empréstimo realizado com sucesso!')
            return redirect('emprestimo_list')
    else:
        form = EmprestimoForm()
        # Filtrar apenas livros disponíveis
        form.fields['livro'].queryset = Livro.objects.filter(disponivel=True)
    return render(request, 'core/emprestimo_form.html', {'form': form})

@login_required
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
    return render(request, 'core/emprestimo_form.html', {'form': form})

@login_required
def emprestimo_delete(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if request.method == 'POST':
        # Marcar livro como disponível novamente
        emprestimo.livro.disponivel = True
        emprestimo.livro.save()
        emprestimo.delete()
        messages.success(request, 'Empréstimo excluído com sucesso!')
        return redirect('emprestimo_list')
    return render(request, 'core/emprestimo_confirm_delete.html', {'emprestimo': emprestimo})

# CRUD CATEGORIAS
@login_required
def categoria_list(request):
    categorias = Categoria.objects.all().order_by('nome')
    return render(request, 'core/categoria_list.html', {'categorias': categorias})

@login_required
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria cadastrada com sucesso!')
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'core/categoria_form.html', {'form': form})

@login_required
def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'core/categoria_form.html', {'form': form})

@login_required
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
        return redirect('categoria_list')
    return render(request, 'core/categoria_confirm_delete.html', {'categoria': categoria})