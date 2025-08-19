from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from app_categoria.models import Categoria
import re

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
