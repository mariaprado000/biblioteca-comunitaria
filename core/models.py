from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import re
from django.core.validators import RegexValidator

def validar_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    if len(cpf) != 11:
        raise ValidationError('CPF deve conter 11 dígitos')
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        raise ValidationError('CPF inválido')
    
    # Calcula o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = 11 - (soma % 11)
    if resto >= 10:
        resto = 0
    if resto != int(cpf[9]):
        raise ValidationError('CPF inválido')
    
    # Calcula o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = 11 - (soma % 11)
    if resto >= 10:
        resto = 0
    if resto != int(cpf[10]):
        raise ValidationError('CPF inválido')
    
def validar_isbn(isbn):
    if not isbn:  # ISBN é opcional
        return
    
    # Remove hífens e espaços
    isbn_limpo = re.sub(r'[-\s]', '', isbn)
    
    if len(isbn_limpo) not in [10, 13]:
        raise ValidationError('ISBN deve ter 10 ou 13 dígitos')
    
    # Verifica se são apenas números (exceto X no final para ISBN-10)
    if len(isbn_limpo) == 10:
        if not isbn_limpo[:-1].isdigit() or (isbn_limpo[-1] not in '0123456789X'):
            raise ValidationError('ISBN-10 inválido')
    else:
        if not isbn_limpo.isdigit():
            raise ValidationError('ISBN-13 deve conter apenas números')
        
class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    ano = models.IntegerField()
    genero = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    isbn = models.CharField(max_length=13, blank=True, validators=[validar_isbn])
    editora = models.CharField(max_length=100, blank=True)
    disponivel = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if self.ano > timezone.now().year:
            raise ValidationError('Ano do livro não pode ser futuro')
        if self.ano < 1000:
            raise ValidationError('Ano inválido')

    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'

telefone_validator = RegexValidator(
    regex=r'^\(\d{2}\)\s?\d{4,5}-\d{4}$',
    message='Telefone deve estar no formato (XX) XXXXX-XXXX ou (XX) XXXX-XXXX'
)
class Leitor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11, unique=True, validators=[validar_cpf])
    telefone = models.CharField(max_length=15, validators=[telefone_validator])
    endereco = models.TextField()
    data_nascimento = models.DateField()
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"
    
    class Meta:
        verbose_name = 'Leitor'
        verbose_name_plural = 'Leitores'

class Funcionario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=50)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    data_admissao = models.DateField()
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name} - {self.cargo}"
    
    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'

class Emprestimo(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    leitor = models.ForeignKey(Leitor, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True)
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao_prevista = models.DateField()
    data_devolucao = models.DateField(null=True, blank=True)
    multa = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    renovacoes = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.livro.titulo} - {self.leitor}"
    
    class Meta:
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'