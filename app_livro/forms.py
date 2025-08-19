from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Livro
from app_categoria.models import Categoria
import re

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'ano', 'genero', 'categoria', 'isbn', 'editora', 'disponivel']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título do livro',
                'required': True
            }),
            'autor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do autor',
                'required': True
            }),
            'ano': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o ano de publicação',
                'required': True,
                'min': 1000,
                'max': timezone.now().year
            }),
            'genero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o gênero do livro',
                'required': True
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o ISBN (opcional)',
                'pattern': '[0-9X-]{10,17}'
            }),
            'editora': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome da editora (opcional)'
            }),
            'disponivel': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'titulo': 'Título',
            'autor': 'Autor',
            'ano': 'Ano de Publicação',
            'genero': 'Gênero',
            'categoria': 'Categoria',
            'isbn': 'ISBN',
            'editora': 'Editora',
            'disponivel': 'Disponível',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configurar o campo categoria
        self.fields['categoria'].queryset = Categoria.objects.all().order_by('nome')
        self.fields['categoria'].empty_label = "Selecione uma categoria (opcional)"
        self.fields['categoria'].required = False

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if not titulo:
            raise forms.ValidationError('Título é obrigatório')
        return titulo.strip()

    def clean_autor(self):
        autor = self.cleaned_data.get('autor')
        if not autor:
            raise forms.ValidationError('Autor é obrigatório')
        return autor.strip()

    def clean_ano(self):
        ano = self.cleaned_data.get('ano')
        if not ano:
            raise forms.ValidationError('Ano de publicação é obrigatório')
        
        current_year = timezone.now().year
        if ano > current_year:
            raise forms.ValidationError('Ano do livro não pode ser futuro')
        if ano < 1000:
            raise forms.ValidationError('Ano inválido')
        
        return ano

    def clean_genero(self):
        genero = self.cleaned_data.get('genero')
        if not genero:
            raise forms.ValidationError('Gênero é obrigatório')
        return genero.strip()

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn', '')
        if not isbn:
            return isbn
        
        # Remove hífens e espaços
        isbn_limpo = re.sub(r'[-\s]', '', isbn)
        
        if len(isbn_limpo) not in [10, 13]:
            raise forms.ValidationError('ISBN deve ter 10 ou 13 dígitos')
        
        # Verifica se são apenas números (exceto X no final para ISBN-10)
        if len(isbn_limpo) == 10:
            if not isbn_limpo[:-1].isdigit() or (isbn_limpo[-1] not in '0123456789X'):
                raise forms.ValidationError('ISBN-10 inválido')
        else:
            if not isbn_limpo.isdigit():
                raise forms.ValidationError('ISBN-13 deve conter apenas números')
        
        # Verifica se já existe um livro com este ISBN (exceto o atual, se estiver editando)
        existing = Livro.objects.filter(isbn=isbn_limpo)
        if self.instance and self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise forms.ValidationError('Já existe um livro cadastrado com este ISBN')
        
        return isbn_limpo

    def clean_editora(self):
        editora = self.cleaned_data.get('editora', '')
        if editora:
            return editora.strip()
        return editora

    def clean(self):
        cleaned_data = super().clean()
        titulo = cleaned_data.get('titulo')
        autor = cleaned_data.get('autor')
        ano = cleaned_data.get('ano')

        # Verificar se já existe um livro com título e autor idênticos
        if titulo and autor and ano:
            existing = Livro.objects.filter(
                titulo__iexact=titulo,
                autor__iexact=autor,
                ano=ano
            )
            if self.instance and self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise forms.ValidationError('Já existe um livro cadastrado com este título, autor e ano')

        return cleaned_data