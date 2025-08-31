from django import forms
from django.contrib.auth.models import User
from .models import Leitor
import re

class LeitorForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Leitor
        fields = ['username', 'first_name', 'last_name', 'email', 'cpf', 'telefone', 'endereco', 'data_nascimento']
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