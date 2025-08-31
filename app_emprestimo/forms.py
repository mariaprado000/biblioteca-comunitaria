from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Emprestimo
from app_livro.models import Livro
from app_leitor.models import Leitor

class EmprestimoForm(forms.ModelForm):
    dias_emprestimo = forms.IntegerField(
        initial=14,
        min_value=1,
        max_value=30,
        label='Dias de Empréstimo',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '14'
        }),
        help_text='Número de dias para o empréstimo (máximo 30 dias)'
    )
    
    class Meta:
        model = Emprestimo
        fields = ['livro', 'leitor']
        widgets = {
            'livro': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'leitor': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
        }
        labels = {
            'livro': 'Livro',
            'leitor': 'Leitor',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas livros disponíveis
        self.fields['livro'].queryset = Livro.objects.filter(disponivel=True).order_by('titulo')
        self.fields['livro'].empty_label = "Selecione um livro"
        
        # Filtrar apenas leitores ativos
        self.fields['leitor'].queryset = Leitor.objects.filter(ativo=True).order_by('usuario__first_name')
        self.fields['leitor'].empty_label = "Selecione um leitor"

    def clean_livro(self):
        livro = self.cleaned_data.get('livro')
        if not livro:
            raise forms.ValidationError('Selecione um livro')
        
        if not livro.disponivel:
            raise forms.ValidationError('Este livro não está disponível para empréstimo')
        
        return livro

    def clean_leitor(self):
        leitor = self.cleaned_data.get('leitor')
        if not leitor:
            raise forms.ValidationError('Selecione um leitor')
        
        if not leitor.ativo:
            raise forms.ValidationError('Este leitor está inativo')
        
        # Verificar se o leitor já tem 3 empréstimos ativos (limite)
        emprestimos_ativos = Emprestimo.objects.filter(
            leitor=leitor,
            data_devolucao__isnull=True
        ).count()
        
        if emprestimos_ativos >= 3:
            raise forms.ValidationError('Este leitor já atingiu o limite de 3 empréstimos simultâneos')
        
        # Verificar se o leitor tem empréstimos atrasados
        emprestimos_atrasados = Emprestimo.objects.filter(
            leitor=leitor,
            data_devolucao__isnull=True,
            data_devolucao_prevista__lt=timezone.now().date()
        ).count()
        
        if emprestimos_atrasados > 0:
            raise forms.ValidationError('Este leitor possui empréstimos em atraso e não pode fazer novos empréstimos')
        
        return leitor

    def clean_dias_emprestimo(self):
        dias = self.cleaned_data.get('dias_emprestimo')
        if not dias:
            return 14  # valor padrão
        
        if dias < 1:
            raise forms.ValidationError('O empréstimo deve ter pelo menos 1 dia')
        
        if dias > 30:
            raise forms.ValidationError('O empréstimo não pode exceder 30 dias')
        
        return dias


class RenovacaoForm(forms.Form):
    dias_renovacao = forms.IntegerField(
        initial=14,
        min_value=1,
        max_value=30,
        label='Dias de Renovação',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '14'
        }),
        help_text='Número de dias para renovar o empréstimo (máximo 30 dias)'
    )

    def __init__(self, emprestimo=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.emprestimo = emprestimo

    def clean_dias_renovacao(self):
        dias = self.cleaned_data.get('dias_renovacao')
        if not dias:
            return 14
        
        if dias < 1:
            raise forms.ValidationError('A renovação deve ter pelo menos 1 dia')
        
        if dias > 30:
            raise forms.ValidationError('A renovação não pode exceder 30 dias')
        
        return dias

    def clean(self):
        cleaned_data = super().clean()
        
        if self.emprestimo:
            # Validar se empréstimo já foi devolvido
            if self.emprestimo.data_devolucao:
                raise forms.ValidationError('Este empréstimo já foi devolvido.')
            
            # Validar se pode ser renovado (não está atrasado e não excedeu limite)
            if not self.emprestimo.pode_renovar():
                raise forms.ValidationError('Este empréstimo não pode ser renovado (atrasado ou limite de renovações atingido).')
        
        return cleaned_data


class DevolucaoForm(forms.Form):
    """Form para confirmação de devolução - apenas para validação"""
    confirmar_devolucao = forms.BooleanField(
        required=True,
        label='Confirmar devolução',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    def __init__(self, emprestimo=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.emprestimo = emprestimo

    def clean_confirmar_devolucao(self):
        confirmado = self.cleaned_data.get('confirmar_devolucao')
        if not confirmado:
            raise forms.ValidationError('É necessário confirmar a devolução')
        return confirmado

    def clean(self):
        cleaned_data = super().clean()
        
        if self.emprestimo:
            # Validar se empréstimo já foi devolvido
            if self.emprestimo.data_devolucao:
                raise forms.ValidationError('Este empréstimo já foi devolvido.')
        
        return cleaned_data