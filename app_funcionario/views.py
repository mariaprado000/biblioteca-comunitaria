from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Funcionario
from .forms import FuncionarioForm

def is_funcionario(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_funcionario)
def funcionario_list(request):
    funcionarios = Funcionario.objects.all().order_by('usuario__first_name')
    return render(request, 'app_funcionario/list.html', {'funcionarios': funcionarios})

@login_required
@user_passes_test(is_funcionario)
def funcionario_create(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário criado com sucesso!')
            return redirect('app_funcionario:list')
    else:
        form = FuncionarioForm()
    return render(request, 'app_funcionario/form.html', {'form': form})

@login_required
@user_passes_test(is_funcionario)
def funcionario_update(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário atualizado com sucesso!')
            return redirect('app_funcionario:list')
    else:
        form = FuncionarioForm(instance=funcionario)
    return render(request, 'app_funcionario/form.html', {'form': form, 'object': funcionario})

@login_required
@user_passes_test(is_funcionario)
def funcionario_delete(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        funcionario.delete()
        messages.success(request, 'Funcionário excluído com sucesso!')
        return redirect('app_funcionario:list')
    return render(request, 'app_funcionario/confirm_delete.html', {'object': funcionario})
