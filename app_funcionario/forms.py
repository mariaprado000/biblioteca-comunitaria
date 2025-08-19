from django import forms
from django.contrib.auth.models import User
from .models import Funcionario

class FuncionarioForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Funcionario
        fields = ['first_name', 'last_name', 'email', 'cargo', 'salario', 'data_admissao']
        widgets = {
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'salario': forms.NumberInput(attrs={'class': 'form-control'}),
            'data_admissao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_salario(self):
        salario = self.cleaned_data['salario']
        
        if salario < 1412:  # Salário mínimo 2024
            raise forms.ValidationError('Salário não pode ser menor que R$ 1.412,00')
        
        if salario > 100000:
            raise forms.ValidationError('Valor de salário inválido (máximo: R$ 100.000,00)')
        
        return salario