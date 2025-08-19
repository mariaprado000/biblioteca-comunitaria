from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Livro
from .forms import LivroForm
from app_categoria.models import Categoria
from biblioteca.decorators import funcionario_or_leitor_required, funcionario_required

@login_required
@funcionario_or_leitor_required
def livro_list(request):
    search = request.GET.get('search', '')
    categoria_id = request.GET.get('categoria', '')
    
    livros = Livro.objects.all()
    
    # Se não for funcionário, mostrar apenas livros disponíveis
    if not request.user.groups.filter(name='Funcionarios').exists():
        livros = livros.filter(disponivel=True)
    
    if search:
        livros = livros.filter(titulo__icontains=search) | livros.filter(autor__icontains=search)
    
    if categoria_id:
        livros = livros.filter(categoria_id=categoria_id)
    
    livros = livros.order_by('titulo')
    categorias = Categoria.objects.all().order_by('nome')
    
    context = {
        'livros': livros,
        'categorias': categorias,
        'search': search,
        'categoria_selecionada': categoria_id
    }
    return render(request, 'app_livro/list.html', context)

@login_required
@funcionario_required
def livro_create(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro criado com sucesso!')
            return redirect('app_livro:listar')
    else:
        form = LivroForm()
    
    categorias = Categoria.objects.all().order_by('nome')
    return render(request, 'app_livro/form.html', {'form': form, 'categorias': categorias})

@login_required
@funcionario_required
def livro_update(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro atualizado com sucesso!')
            return redirect('app_livro:listar')
    else:
        form = LivroForm(instance=livro)
    
    categorias = Categoria.objects.all().order_by('nome')
    return render(request, 'app_livro/form.html', {'form': form, 'object': livro, 'categorias': categorias})

@login_required
@funcionario_required
def livro_delete(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        livro.delete()
        messages.success(request, 'Livro excluído com sucesso!')
        return redirect('app_livro:listar')
    return render(request, 'app_livro/confirm_delete.html', {'object': livro})
