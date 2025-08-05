from django import forms
from .models import Livro, Categoria

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'ano', 'genero', 'categoria', 'isbn', 'editora', 'disponivel']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'genero': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'editora': forms.TextInput(attrs={'class': 'form-control'}),
            'disponivel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }