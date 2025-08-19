from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Leitor
from .forms import LeitorForm

def is_funcionario(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_funcionario)
def leitor_list(request):
    leitores = Leitor.objects.all().order_by('usuario__first_name')
    return render(request, 'app_leitor/list.html', {'leitores': leitores})

@login_required
@user_passes_test(is_funcionario)
def leitor_create(request):
    if request.method == 'POST':
        form = LeitorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leitor criado com sucesso!')
            return redirect('app_leitor:list')
    else:
        form = LeitorForm()
    return render(request, 'app_leitor/form.html', {'form': form})

@login_required
@user_passes_test(is_funcionario)
def leitor_update(request, pk):
    leitor = get_object_or_404(Leitor, pk=pk)
    if request.method == 'POST':
        form = LeitorForm(request.POST, instance=leitor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leitor atualizado com sucesso!')
            return redirect('app_leitor:list')
    else:
        form = LeitorForm(instance=leitor)
    return render(request, 'app_leitor/form.html', {'form': form, 'object': leitor})

@login_required
@user_passes_test(is_funcionario)
def leitor_delete(request, pk):
    leitor = get_object_or_404(Leitor, pk=pk)
    if request.method == 'POST':
        leitor.delete()
        messages.success(request, 'Leitor excluído com sucesso!')
        return redirect('app_leitor:list')
    return render(request, 'app_leitor/confirm_delete.html', {'object': leitor})
