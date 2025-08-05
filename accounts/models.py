from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re

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