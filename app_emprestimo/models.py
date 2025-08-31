from django.db import models
from django.utils import timezone
from decimal import Decimal
from app_livro.models import Livro
from app_leitor.models import Leitor
from app_funcionario.models import Funcionario

class Emprestimo(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    leitor = models.ForeignKey(Leitor, on_delete=models.CASCADE)
    emprestado_por = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, related_name='emprestimos_registrados')
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao_prevista = models.DateField()
    data_devolucao = models.DateField(null=True, blank=True)
    multa = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    renovacao = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='renovacoes')
    
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
    
    def contar_renovacoes(self):
        """Conta quantas renovações foram feitas recursivamente"""
        count = 0
        emprestimo_atual = self
        while emprestimo_atual.renovacao:
            count += 1
            emprestimo_atual = emprestimo_atual.renovacao
        return count
    
    def get_emprestimo_original(self):
        """Retorna o empréstimo original (raiz da cadeia de renovações)"""
        emprestimo_atual = self
        while emprestimo_atual.renovacao:
            emprestimo_atual = emprestimo_atual.renovacao
        return emprestimo_atual
    
    def pode_renovar(self):
        """Verifica se o empréstimo pode ser renovado"""
        # Não pode renovar se está atrasado ou já foi renovado 2 vezes
        return not self.esta_atrasado() and self.contar_renovacoes() < 2
    
    def __str__(self):
        return f"{self.livro.titulo} - {self.leitor}"
    
    class Meta:
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'
        ordering = ['-data_emprestimo']
