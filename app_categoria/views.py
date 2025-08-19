from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Categoria
from biblioteca.decorators import funcionario_or_leitor_required, funcionario_required

@login_required
@funcionario_or_leitor_required
def categoria_list(request):
    search = request.GET.get('search', '')
    if search:
        categorias = Categoria.objects.filter(nome__icontains=search).order_by('nome')
    else:
        categorias = Categoria.objects.all().order_by('nome')
    
    context = {
        'categorias': categorias,
        'search': search
    }
    return render(request, 'app_categoria/list.html', context)

@login_required
@funcionario_required
def categoria_create(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        Categoria.objects.create(nome=nome, descricao=descricao)
        messages.success(request, 'Categoria criada com sucesso!')
        return redirect('app_categoria:listar')
    return render(request, 'app_categoria/form.html')

@login_required
@funcionario_required
def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.nome = request.POST.get('nome')
        categoria.descricao = request.POST.get('descricao', '')
        categoria.save()
        messages.success(request, 'Categoria atualizada com sucesso!')
        return redirect('app_categoria:listar')
    return render(request, 'app_categoria/form.html', {'object': categoria})

@login_required
@funcionario_required
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
        return redirect('app_categoria:listar')
    return render(request, 'app_categoria/confirm_delete.html', {'object': categoria})
