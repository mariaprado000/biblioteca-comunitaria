from accounts.models import Leitor, Funcionario
from appbiblioteca.models import Livro
from django.db import models
from django.utils import timezone
from decimal import Decimal

# Temporariamente importando de core - mudar depois quando migrarmos tudo

class Emprestimo(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    leitor = models.ForeignKey(Leitor, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True)
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao_prevista = models.DateField()
    data_devolucao = models.DateField(null=True, blank=True)
    multa = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    renovacoes = models.IntegerField(default=0)
    
    def calcular_multa(self):
        """Calcula a multa baseada nos dias de atraso"""
        if not self.data_devolucao and self.data_devolucao_prevista < timezone.now().date():
            dias_atraso = (timezone.now().date() - self.data_devolucao_prevista).days
            return Decimal(str(dias_atraso * 2.00))
        elif self.data_devolucao and self.data_devolucao > self.data_devolucao_prevista:
            dias_atraso = (self.data_devolucao - self.data_devolucao_prevista).days
            return Decimal(str(dias_atraso * 2.00))
        return Decimal('0.00')
    
    def esta_atrasado(self):
        """Verifica se o empréstimo está atrasado"""
        return not self.data_devolucao and self.data_devolucao_prevista < timezone.now().date()
    
    def pode_renovar(self):
        """Verifica se o empréstimo pode ser renovado"""
        # Não pode renovar se está atrasado ou já foi renovado 2 vezes
        return not self.esta_atrasado() and self.renovacoes < 2
    
    def __str__(self):
        return f"{self.livro.titulo} - {self.leitor}"
    
    class Meta:
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'
        ordering = ['-data_emprestimo']

