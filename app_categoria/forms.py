from django import forms
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome da categoria',
                'required': True
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Digite a descrição da categoria (opcional)',
                'rows': 3
            }),
        }
        labels = {
            'nome': 'Nome da Categoria',
            'descricao': 'Descrição',
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if not nome:
            raise forms.ValidationError('Nome da categoria é obrigatório')
        
        # Verificar se já existe uma categoria com este nome (exceto a atual, se estiver editando)
        existing = Categoria.objects.filter(nome__iexact=nome)
        if self.instance and self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise forms.ValidationError('Já existe uma categoria com este nome')
        
        return nome.strip().title()  # Remove espaços e capitaliza

    def clean_descricao(self):
        descricao = self.cleaned_data.get('descricao', '')
        if descricao:
            return descricao.strip()
        return descricao