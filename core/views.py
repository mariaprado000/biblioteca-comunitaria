from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.db.models import Count, Q
from django.db import transaction 
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import Livro, Leitor, Funcionario, Emprestimo, Categoria
from .forms import LivroForm, LeitorForm, FuncionarioForm, EmprestimoForm, CategoriaForm, RegistroForm

# Funções auxiliares para verificar grupos
def is_funcionario(user):
    return user.groups.filter(name='Funcionários').exists() or user.is_superuser

def is_leitor(user):
    return user.groups.filter(name='Leitores').exists()

# View Home com Dashboard
@login_required
def home(request):
    context = {}
    
    if is_funcionario(request.user):
        # Dashboard para funcionários
        context['total_livros'] = Livro.objects.count()
        context['livros_disponiveis'] = Livro.objects.filter(disponivel=True).count()
        context['total_leitores'] = Leitor.objects.filter(ativo=True).count()
        context['emprestimos_ativos'] = Emprestimo.objects.filter(data_devolucao__isnull=True).count()
        context['emprestimos_atrasados'] = Emprestimo.objects.filter(
            data_devolucao__isnull=True,
            data_devolucao_prevista__lt=timezone.now().date()
        ).count()
        
        # Livros mais emprestados
        context['livros_populares'] = Livro.objects.annotate(
            num_emprestimos=Count('emprestimo')
        ).order_by('-num_emprestimos')[:5]
        
    else:
        # Dashboard para leitores
        try:
            leitor = request.user.leitor
            context['meus_emprestimos'] = Emprestimo.objects.filter(
                leitor=leitor,
                data_devolucao__isnull=True
            )
            context['historico_emprestimos'] = Emprestimo.objects.filter(
                leitor=leitor
            ).order_by('-data_emprestimo')[:10]
        except:
            pass
    
    return render(request, 'core/home.html', context)

# View Registro
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Adicionar usuário ao grupo padrão
            try:
                grupo_leitores = Group.objects.get(name='Leitores')
                user.groups.add(grupo_leitores)
            except Group.DoesNotExist:
                pass
            login(request, user)
            messages.success(request, 'Registro realizado com sucesso! Complete seu cadastro como leitor.')
            return redirect('leitor_create_self')
    else:
        form = RegistroForm()
    return render(request, 'core/registro.html', {'form': form})

# CRUD LIVROS (apenas funcionários)
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
    return render(request, 'core/livro_list.html', {'livros': livros, 'query': query})

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
    return render(request, 'core/livro_form.html', {'form': form})

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
    return render(request, 'core/livro_form.html', {'form': form})

@login_required
@user_passes_test(is_funcionario)
def livro_delete(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        livro.delete()
        messages.success(request, 'Livro excluído com sucesso!')
        return redirect('livro_list')
    return render(request, 'core/livro_confirm_delete.html', {'livro': livro})

# CRUD LEITORES
@login_required
@user_passes_test(is_funcionario)
def leitor_list(request):
    query = request.GET.get('q')
    if query:
        leitores = Leitor.objects.filter(
            Q(usuario__first_name__icontains=query) |
            Q(usuario__last_name__icontains=query) |
            Q(cpf__icontains=query)
        ).order_by('usuario__first_name')
    else:
        leitores = Leitor.objects.all().order_by('usuario__first_name')
    return render(request, 'core/leitor_list.html', {'leitores': leitores, 'query': query})

@login_required
def leitor_create_self(request):
    """Permite que um usuário recém-registrado crie seu próprio perfil de leitor"""
    if hasattr(request.user, 'leitor'):
        messages.info(request, 'Você já possui um cadastro de leitor.')
        return redirect('home')
    
    if request.method == 'POST':
        form = LeitorForm(request.POST)
        if form.is_valid():
            leitor = form.save(commit=False)
            leitor.usuario = request.user
            # Atualizar dados do usuário
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            leitor.save()
            messages.success(request, 'Cadastro de leitor concluído com sucesso!')
            return redirect('home')
    else:
        form = LeitorForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
    return render(request, 'core/leitor_form.html', {'form': form, 'self_register': True})

@login_required
@user_passes_test(is_funcionario)
def leitor_create(request):
    if request.method == 'POST':
        form = LeitorForm(request.POST)
        if form.is_valid():
            # Criar usuário
            username = form.cleaned_data['cpf']
            user = User.objects.create_user(
                username=username,
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password='senha123'
            )
            # Adicionar ao grupo Leitores
            try:
                grupo_leitores = Group.objects.get(name='Leitores')
                user.groups.add(grupo_leitores)
            except Group.DoesNotExist:
                pass
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
@user_passes_test(is_funcionario)
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
@user_passes_test(is_funcionario)
def leitor_delete(request, pk):
    leitor = get_object_or_404(Leitor, pk=pk)
    if request.method == 'POST':
        leitor.usuario.delete()
        messages.success(request, 'Leitor excluído com sucesso!')
        return redirect('leitor_list')
    return render(request, 'core/leitor_confirm_delete.html', {'leitor': leitor})

# CRUD FUNCIONÁRIOS (apenas funcionários)
@login_required
@user_passes_test(is_funcionario)
def funcionario_list(request):
    funcionarios = Funcionario.objects.all().order_by('usuario__first_name')
    return render(request, 'core/funcionario_list.html', {'funcionarios': funcionarios})

@login_required
@user_passes_test(is_funcionario)
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
                password='senha123'
            )
            user.is_staff = True
            user.save()
            # Adicionar ao grupo Funcionários
            try:
                grupo_funcionarios = Group.objects.get(name='Funcionários')
                user.groups.add(grupo_funcionarios)
            except Group.DoesNotExist:
                pass
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
@user_passes_test(is_funcionario)
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
@user_passes_test(is_funcionario)
def funcionario_delete(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        funcionario.usuario.delete()
        messages.success(request, 'Funcionário excluído com sucesso!')
        return redirect('funcionario_list')
    return render(request, 'core/funcionario_confirm_delete.html', {'funcionario': funcionario})

# CRUD EMPRÉSTIMOS
@login_required
def emprestimo_list(request):
    emprestimos_atrasados = 0  # Inicializar a variável
    
    if is_funcionario(request.user):
        emprestimos = Emprestimo.objects.all().order_by('-data_emprestimo')
        # Contar empréstimos atrasados
        emprestimos_atrasados = Emprestimo.objects.filter(
            data_devolucao__isnull=True,
            data_devolucao_prevista__lt=timezone.now().date()
        ).count()
    else:
        try:
            leitor = request.user.leitor
            emprestimos = Emprestimo.objects.filter(leitor=leitor).order_by('-data_emprestimo')
        except:
            emprestimos = Emprestimo.objects.none()
    
    # Calcular multas
    for emprestimo in emprestimos:
        if not emprestimo.data_devolucao and emprestimo.data_devolucao_prevista < timezone.now().date():
            dias_atraso = (timezone.now().date() - emprestimo.data_devolucao_prevista).days
            emprestimo.multa = Decimal(dias_atraso * 2.00)  # R$ 2,00 por dia de atraso
            emprestimo.save()
    
    return render(request, 'core/emprestimo_list.html', {
        'emprestimos': emprestimos,
        'emprestimos_atrasados': emprestimos_atrasados,
        'today': timezone.now().date()
    })

@login_required
@user_passes_test(is_funcionario)
def emprestimo_create(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo = form.save(commit=False)
            
            # ADICIONAR: Verificação mais segura
            livro = Livro.objects.select_for_update().get(pk=emprestimo.livro.pk)
            
            if not livro.disponivel:
                messages.error(request, 'Este livro já está emprestado!')
                form = EmprestimoForm()  # Resetar o form
                form.fields['livro'].queryset = Livro.objects.filter(disponivel=True)
                return render(request, 'core/emprestimo_form.html', {'form': form})
            
            # ADICIONAR: Verificar limite de empréstimos
            emprestimos_ativos = Emprestimo.objects.filter(
                leitor=emprestimo.leitor,
                data_devolucao__isnull=True
            ).count()
            
            if emprestimos_ativos >= 3:  # Limite de 3 livros
                messages.error(request, 'Este leitor já possui 3 livros emprestados!')
                return redirect('emprestimo_create')
            
            # Verificar empréstimos em atraso (já existe mas melhorar)
            emprestimos_atraso = Emprestimo.objects.filter(
                leitor=emprestimo.leitor,
                data_devolucao__isnull=True,
                data_devolucao_prevista__lt=timezone.now().date()
            )
            
            if emprestimos_atraso.exists():
                livros_atrasados = ', '.join([e.livro.titulo for e in emprestimos_atraso])
                messages.warning(request, f'ATENÇÃO: Este leitor possui os seguintes livros em atraso: {livros_atrasados}')

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
@user_passes_test(is_funcionario)
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
@user_passes_test(is_funcionario)
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

@login_required
@user_passes_test(is_funcionario)
def emprestimo_devolver(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    
    if request.method == 'POST':
        emprestimo.data_devolucao = timezone.now().date()
        
        # MELHORAR: Cálculo de multa mais claro
        if emprestimo.data_devolucao > emprestimo.data_devolucao_prevista:
            dias_atraso = (emprestimo.data_devolucao - emprestimo.data_devolucao_prevista).days
            emprestimo.multa = Decimal(str(dias_atraso * 2.00))  # Usar string para Decimal
            
            # Log para debug
            print(f"Dias atraso: {dias_atraso}, Multa: {emprestimo.multa}")
        else:
            emprestimo.multa = Decimal('0.00')
        
        emprestimo.save()
        return redirect('emprestimo_list')
    return render(request, 'core/emprestimo_devolver.html', {'emprestimo': emprestimo})

@login_required
def emprestimo_renovar(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    
    # Verificar se o usuário pode renovar
    if not is_funcionario(request.user):
        try:
            leitor = request.user.leitor
            if emprestimo.leitor != leitor:
                messages.error(request, 'Você só pode renovar seus próprios empréstimos!')
                return redirect('emprestimo_list')
        except:
            messages.error(request, 'Acesso negado!')
            return redirect('home')
    
    if request.method == 'POST':
            # Verificar se não está em atraso
            if emprestimo.data_devolucao_prevista < timezone.now().date():
                messages.error(request, 'Não é possível renovar empréstimos em atraso!')
                return redirect('emprestimo_list')
            
            
            # Renovar por mais 14 dias
            nova_data = emprestimo.data_devolucao_prevista + timedelta(days=14)
            
            # ADICIONAR: Verificar se não ultrapassa 60 dias totais
            dias_totais = (nova_data - emprestimo.data_emprestimo.date()).days
            if dias_totais > 60:
                messages.error(request, 'O empréstimo não pode exceder 60 dias no total!')
                return redirect('emprestimo_list')
            
            emprestimo.data_devolucao_prevista = nova_data
            emprestimo.save()
            messages.success(request, f'Empréstimo renovado até {nova_data.strftime("%d/%m/%Y")}!')
            return redirect('emprestimo_list')
    
# CRUD CATEGORIAS (apenas funcionários)
@login_required
@user_passes_test(is_funcionario)
def categoria_list(request):
    categorias = Categoria.objects.all().order_by('nome')
    return render(request, 'core/categoria_list.html', {'categorias': categorias})

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
    return render(request, 'core/categoria_form.html', {'form': form})

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
    return render(request, 'core/categoria_form.html', {'form': form})

@login_required
@user_passes_test(is_funcionario)
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
        return redirect('categoria_list')
    return render(request, 'core/categoria_confirm_delete.html', {'categoria': categoria})

# Views de relatórios
@login_required
@user_passes_test(is_funcionario)
def relatorio_livros_populares(request):
    livros = Livro.objects.annotate(
        num_emprestimos=Count('emprestimo')
    ).order_by('-num_emprestimos')[:10]
    return render(request, 'core/relatorio_livros_populares.html', {'livros': livros})

@login_required
@user_passes_test(is_funcionario)
def relatorio_atrasos(request):
    emprestimos_atraso = Emprestimo.objects.filter(
        data_devolucao__isnull=True,
        data_devolucao_prevista__lt=timezone.now().date()
    ).order_by('data_devolucao_prevista')
    
    # Calcular multas
    for emprestimo in emprestimos_atraso:
        dias_atraso = (timezone.now().date() - emprestimo.data_devolucao_prevista).days
        emprestimo.multa_atual = Decimal(dias_atraso * 2.00)
    
    return render(request, 'core/relatorio_atrasos.html', {'emprestimos': emprestimos_atraso})