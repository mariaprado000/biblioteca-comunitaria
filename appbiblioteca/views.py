from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Livro, Categoria
from .forms import LivroForm, CategoriaForm

# Função auxiliar para verificar se é funcionário
def is_funcionario(user):
    return user.groups.filter(name='Funcionários').exists() or user.is_superuser

# CRUD LIVROS
@login_required
def livro_list(request):
    query = request.GET.get('q')
    if query:
        livros = Livro.objects.filter(
            Q(titulo__icontains=query) | 
            Q(autor__icontains=query) |
            Q(isbn__icontains=query)
        ).order_by('titulo')
    else:
        livros = Livro.objects.all().order_by('titulo')
    return render(request, 'appbiblioteca/livro_list.html', {'livros': livros, 'query': query})

@login_required
@user_passes_test(is_funcionario)
def livro_create(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro cadastrado com sucesso!')
            return redirect('livro_list')
    else:
        form = LivroForm()
    return render(request, 'appbiblioteca/livro_form.html', {'form': form})

@login_required
@user_passes_test(is_funcionario)
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
    return render(request, 'appbiblioteca/livro_form.html', {'form': form})

@login_required
@user_passes_test(is_funcionario)
def livro_delete(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        livro.delete()
        messages.success(request, 'Livro excluído com sucesso!')
        return redirect('livro_list')
    return render(request, 'appbiblioteca/livro_confirm_delete.html', {'livro': livro})

# CRUD CATEGORIAS
@login_required
@user_passes_test(is_funcionario)
def categoria_list(request):
    categorias = Categoria.objects.all().order_by('nome')
    return render(request, 'appbiblioteca/categoria_list.html', {'categorias': categorias})

@login_required
@user_passes_test(is_funcionario)
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria cadastrada com sucesso!')
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'appbiblioteca/categoria_form.html', {'form': form})

@login_required
@user_passes_test(is_funcionario)
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
    return render(request, 'appbiblioteca/categoria_form.html', {'form': form})

@login_required
@user_passes_test(is_funcionario)
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
        return redirect('categoria_list')
    return render(request, 'appbiblioteca/categoria_confirm_delete.html', {'categoria': categoria})