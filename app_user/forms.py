from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from app_leitor.models import Leitor

class LeitorRegistrationForm(UserCreationForm):
    # Dados pessoais
    first_name = forms.CharField(
        max_length=30,
        label='Nome',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        label='Sobrenome',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu sobrenome'
        })
    )
    
    email = forms.EmailField(
        required=False,
        label='E-mail (opcional)',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu e-mail'
        })
    )
    
    # Dados específicos do leitor
    cpf = forms.CharField(
        max_length=14,
        label='CPF',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '000.000.000-00',
            'pattern': '[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}-?[0-9]{2}'
        })
    )
    
    telefone = forms.CharField(
        max_length=15,
        required=False,
        label='Telefone (opcional)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(00) 00000-0000'
        })
    )
    
    endereco = forms.CharField(
        max_length=200,
        required=False,
        label='Endereço (opcional)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu endereço'
        })
    )
    
    data_nascimento = forms.DateField(
        label='Data de Nascimento',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar classes Bootstrap aos campos padrão
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite seu nome de usuário'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '••••••••••••'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '••••••••••••'
        })

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            # Remove pontos e traços
            cpf = cpf.replace('.', '').replace('-', '')
            # Verifica se já existe
            if Leitor.objects.filter(cpf=cpf).exists():
                raise forms.ValidationError('Este CPF já está cadastrado.')
        return cpf

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            
            # Adicionar ao grupo de Leitores
            leitores_group, created = Group.objects.get_or_create(name='Leitores')
            user.groups.add(leitores_group)
            
            # Criar perfil de leitor
            leitor = Leitor.objects.create(
                pk=user.pk,
                cpf=self.cleaned_data['cpf'].replace('.', '').replace('-', ''),
                telefone=self.cleaned_data.get('telefone', ''),
                endereco=self.cleaned_data.get('endereco', ''),
                data_nascimento=self.cleaned_data['data_nascimento'],
                ativo=True
            )
            
        return user