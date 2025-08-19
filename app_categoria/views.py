from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Categoria

def is_funcionario(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_funcionario)
def categoria_list(request):
    categorias = Categoria.objects.all().order_by('nome')
    return render(request, 'app_categoria/list.html', {'categorias': categorias})

@login_required
@user_passes_test(is_funcionario)
def categoria_create(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        Categoria.objects.create(nome=nome, descricao=descricao)
        messages.success(request, 'Categoria criada com sucesso!')
        return redirect('app_categoria:list')
    return render(request, 'app_categoria/form.html')

@login_required
@user_passes_test(is_funcionario)
def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.nome = request.POST.get('nome')
        categoria.descricao = request.POST.get('descricao', '')
        categoria.save()
        messages.success(request, 'Categoria atualizada com sucesso!')
        return redirect('app_categoria:list')
    return render(request, 'app_categoria/form.html', {'object': categoria})

@login_required
@user_passes_test(is_funcionario)
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
        return redirect('app_categoria:list')
    return render(request, 'app_categoria/confirm_delete.html', {'object': categoria})
