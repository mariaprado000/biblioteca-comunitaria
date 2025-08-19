"""
Decorators para controle de acesso baseado em grupos
"""

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from functools import wraps

def funcionario_required(view_func):
    """
    Decorator que permite acesso apenas para usuários do grupo 'Funcionarios'
    """
    def check_funcionario(user):
        if not user.is_authenticated:
            return False
        return user.groups.filter(name='Funcionarios').exists()
    
    return user_passes_test(check_funcionario)(view_func)

def leitor_required(view_func):
    """
    Decorator que permite acesso apenas para usuários do grupo 'Leitores'
    """
    def check_leitor(user):
        if not user.is_authenticated:
            return False
        return user.groups.filter(name='Leitores').exists()
    
    return user_passes_test(check_leitor)(view_func)

def funcionario_or_leitor_required(view_func):
    """
    Decorator que permite acesso para usuários dos grupos 'Funcionarios' ou 'Leitores'
    """
    def check_funcionario_or_leitor(user):
        if not user.is_authenticated:
            return False
        return user.groups.filter(name__in=['Funcionarios', 'Leitores']).exists()
    
    return user_passes_test(check_funcionario_or_leitor)(view_func)

class FuncionarioRequiredMixin(UserPassesTestMixin):
    """
    Mixin para Class-Based Views que requer usuário do grupo 'Funcionarios'
    """
    def test_func(self):
        return self.request.user.is_authenticated and \
               self.request.user.groups.filter(name='Funcionarios').exists()

class LeitorRequiredMixin(UserPassesTestMixin):
    """
    Mixin para Class-Based Views que requer usuário do grupo 'Leitores'
    """
    def test_func(self):
        return self.request.user.is_authenticated and \
               self.request.user.groups.filter(name='Leitores').exists()

class FuncionarioOrLeitorRequiredMixin(UserPassesTestMixin):
    """
    Mixin para Class-Based Views que requer usuário dos grupos 'Funcionarios' ou 'Leitores'
    """
    def test_func(self):
        return self.request.user.is_authenticated and \
               self.request.user.groups.filter(name__in=['Funcionarios', 'Leitores']).exists()