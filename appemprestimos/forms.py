from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Emprestimo

# Temporariamente importando de core
from appbiblioteca.models import Livro

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['livro', 'leitor', 'data_devolucao_prevista']
        widgets = {
            'livro': forms.Select(attrs={'class': 'form-control'}),
            'leitor': forms.Select(attrs={'class': 'form-control'}),
            'data_devolucao_prevista': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se está criando um novo empréstimo, filtrar apenas livros disponíveis
        if not self.instance.pk:
            self.fields['livro'].queryset = Livro.objects.filter(disponivel=True)
    
    def clean_data_devolucao_prevista(self):
        data = self.cleaned_data['data_devolucao_prevista']
        
        if data < timezone.now().date():
            raise forms.ValidationError('A data de devolução não pode ser no passado!')
        
        if data > timezone.now().date() + timedelta(days=30):
            raise forms.ValidationError('O prazo máximo de empréstimo é de 30 dias!')
        
        return data
    
    def clean(self):
        cleaned_data = super().clean()
        leitor = cleaned_data.get('leitor')
        
        if leitor and self.instance.pk is None:  # Novo empréstimo
            # Verificar se o leitor tem empréstimos em atraso
            emprestimos_atraso = Emprestimo.objects.filter(
                leitor=leitor,
                data_devolucao__isnull=True,
                data_devolucao_prevista__lt=timezone.now().date()
            ).exists()
            
            if emprestimos_atraso:
                raise forms.ValidationError('Este leitor possui empréstimos em atraso e não pode fazer novos empréstimos.')
            
            # Verificar limite de empréstimos ativos (máximo 3)
            emprestimos_ativos = Emprestimo.objects.filter(
                leitor=leitor,
                data_devolucao__isnull=True
            ).count()
            
            if emprestimos_ativos >= 3:
                raise forms.ValidationError('Este leitor já possui 3 livros emprestados (limite máximo).')
        
        return cleaned_data

