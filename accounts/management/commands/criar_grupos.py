from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import Leitor, Funcionario
from appbiblioteca.models import Livro, Categoria
from appemprestimos.models import Emprestimo

class Command(BaseCommand):
    help = 'Cria grupos de permissão para o sistema'

    def handle(self, *args, **kwargs):
        # Criar grupo Leitores
        leitores_group, created = Group.objects.get_or_create(name='Leitores')
        if created:
            self.stdout.write(self.style.SUCCESS('Grupo "Leitores" criado com sucesso!'))
        else:
            self.stdout.write('Grupo "Leitores" já existe.')
            
        # Permissões básicas para leitores
        try:
            # Leitores podem ver livros
            livro_ct = ContentType.objects.get_for_model(Livro)
            perms = Permission.objects.filter(
                content_type=livro_ct,
                codename__in=['view_livro']
            )
            leitores_group.permissions.add(*perms)
            
            # Leitores podem ver seus próprios empréstimos
            emprestimo_ct = ContentType.objects.get_for_model(Emprestimo)
            perms = Permission.objects.filter(
                content_type=emprestimo_ct,
                codename__in=['view_emprestimo']
            )
            leitores_group.permissions.add(*perms)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Erro ao adicionar permissões: {e}'))
        
        # Criar grupo Funcionários
        funcionarios_group, created = Group.objects.get_or_create(name='Funcionários')
        if created:
            self.stdout.write(self.style.SUCCESS('Grupo "Funcionários" criado com sucesso!'))
        else:
            self.stdout.write('Grupo "Funcionários" já existe.')
            
        # Funcionários têm todas as permissões dos modelos relevantes
        try:
            for model in [Livro, Leitor, Funcionario, Emprestimo, Categoria]:
                ct = ContentType.objects.get_for_model(model)
                permissions = Permission.objects.filter(content_type=ct)
                funcionarios_group.permissions.add(*permissions)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Erro ao adicionar permissões: {e}'))
            
        self.stdout.write(self.style.SUCCESS('Grupos configurados com sucesso!'))
