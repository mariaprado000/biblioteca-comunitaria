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

def validar_telefone(telefone):
    # Remove todos os caracteres não numéricos
    apenas_numeros = re.sub(r'[^0-9]', '', telefone)
    
    # Deve ter entre 10 e 11 dígitos (com DDD)
    if len(apenas_numeros) < 10 or len(apenas_numeros) > 11:
        raise ValidationError('Telefone deve ter 10 ou 11 dígitos (incluindo DDD)')

class Leitor(User):
    cpf = models.CharField(max_length=11, unique=True, validators=[validar_cpf])
    telefone = models.CharField(max_length=15, validators=[validar_telefone])
    endereco = models.TextField()
    data_nascimento = models.DateField()
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = 'Leitor'
        verbose_name_plural = 'Leitores'
