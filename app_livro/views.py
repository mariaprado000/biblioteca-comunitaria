from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Livro
from app_categoria.models import Categoria

def is_funcionario(user):
    return user.is_staff or user.is_superuser

@login_required
def livro_list(request):
    search = request.GET.get('search', '')
    categoria_id = request.GET.get('categoria', '')
    
    livros = Livro.objects.all()
    
    # Se não for funcionário, mostrar apenas livros disponíveis
    if not (request.user.is_staff or request.user.is_superuser):
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
@user_passes_test(is_funcionario)
def livro_create(request):
    if request.method == 'POST':
        try:
            livro = Livro(
                titulo=request.POST.get('titulo'),
                autor=request.POST.get('autor'),
                ano=int(request.POST.get('ano')),
                genero=request.POST.get('genero'),
                isbn=request.POST.get('isbn', ''),
                editora=request.POST.get('editora', '')
            )
            
            categoria_id = request.POST.get('categoria')
            if categoria_id:
                livro.categoria_id = categoria_id
            
            livro.full_clean()
            livro.save()
            messages.success(request, 'Livro criado com sucesso!')
            return redirect('app_livro:listar')
        except (ValueError, ValidationError) as e:
            messages.error(request, f'Erro ao criar livro: {e}')
    
    categorias = Categoria.objects.all().order_by('nome')
    return render(request, 'app_livro/form.html', {'categorias': categorias})

@login_required
@user_passes_test(is_funcionario)
def livro_update(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    
    if request.method == 'POST':
        try:
            livro.titulo = request.POST.get('titulo')
            livro.autor = request.POST.get('autor')
            livro.ano = int(request.POST.get('ano'))
            livro.genero = request.POST.get('genero')
            livro.isbn = request.POST.get('isbn', '')
            livro.editora = request.POST.get('editora', '')
            
            categoria_id = request.POST.get('categoria')
            if categoria_id:
                livro.categoria_id = categoria_id
            else:
                livro.categoria = None
            
            livro.full_clean()
            livro.save()
            messages.success(request, 'Livro atualizado com sucesso!')
            return redirect('app_livro:listar')
        except (ValueError, ValidationError) as e:
            messages.error(request, f'Erro ao atualizar livro: {e}')
    
    categorias = Categoria.objects.all().order_by('nome')
    return render(request, 'app_livro/form.html', {'object': livro, 'categorias': categorias})

@login_required
@user_passes_test(is_funcionario)
def livro_delete(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        livro.delete()
        messages.success(request, 'Livro excluído com sucesso!')
        return redirect('app_livro:listar')
    return render(request, 'app_livro/confirm_delete.html', {'object': livro})
