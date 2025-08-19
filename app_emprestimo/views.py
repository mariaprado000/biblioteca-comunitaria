from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Emprestimo

def is_funcionario(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_funcionario)
def emprestimo_list(request):
    emprestimos = Emprestimo.objects.all().order_by('-data_emprestimo')
    return render(request, 'app_emprestimo/list.html', {'emprestimos': emprestimos})

@login_required
@user_passes_test(is_funcionario)
def emprestimo_create(request):
    return render(request, 'app_emprestimo/form.html')

@login_required
@user_passes_test(is_funcionario)
def emprestimo_devolver(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    return render(request, 'app_emprestimo/devolver.html', {'object': emprestimo})

@login_required
@user_passes_test(is_funcionario)
def emprestimo_renovar(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    return render(request, 'app_emprestimo/renovar.html', {'object': emprestimo})
