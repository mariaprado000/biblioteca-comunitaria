from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Leitor, Funcionario
import re

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class LeitorForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Leitor
        fields = ['first_name', 'last_name', 'email', 'cpf', 'telefone', 'endereco', 'data_nascimento']
        widgets = {
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def clean_data_nascimento(self):
        from django.utils import timezone
        data = self.cleaned_data['data_nascimento']
        idade = (timezone.now().date() - data).days / 365.25
        
        if idade < 10:
            raise forms.ValidationError('Leitor deve ter pelo menos 10 anos')
        if idade > 120:
            raise forms.ValidationError('Data de nascimento inválida')
        
        return data
    
    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        # Remove pontos e traços se o usuário digitou
        cpf = re.sub(r'[^0-9]', '', cpf)
        return cpf

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