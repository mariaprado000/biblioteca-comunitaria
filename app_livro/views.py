from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Livro

def is_funcionario(user):
    return user.is_staff or user.is_superuser

@login_required
def livro_list(request):
    livros = Livro.objects.all().order_by('titulo')
    return render(request, 'app_livro/list.html', {'livros': livros})

@login_required
@user_passes_test(is_funcionario)
def livro_create(request):
    return render(request, 'app_livro/form.html')

@login_required
@user_passes_test(is_funcionario)
def livro_update(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    return render(request, 'app_livro/form.html', {'object': livro})

@login_required
@user_passes_test(is_funcionario)
def livro_delete(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        livro.delete()
        messages.success(request, 'Livro excluído com sucesso!')
        return redirect('app_livro:list')
    return render(request, 'app_livro/confirm_delete.html', {'object': livro})
