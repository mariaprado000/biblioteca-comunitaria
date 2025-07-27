from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Livro, Leitor, Funcionario, Emprestimo, Categoria

class Command(BaseCommand):
    help = 'Cria grupos de permissão para o sistema'

    def handle(self, *args, **kwargs):
        # Criar grupo Leitores
        leitores_group, created = Group.objects.get_or_create(name='Leitores')
        if created:
            # Permissões básicas para leitores
            livro_ct = ContentType.objects.get_for_model(Livro)
            emprestimo_ct = ContentType.objects.get_for_model(Emprestimo)
            
            # Leitores podem ver livros
            perm = Permission.objects.get(content_type=livro_ct, codename='view_livro')
            leitores_group.permissions.add(perm)
            
            # Leitores podem ver seus empréstimos
            perm = Permission.objects.get(content_type=emprestimo_ct, codename='view_emprestimo')
            leitores_group.permissions.add(perm)
            
            self.stdout.write(self.style.SUCCESS('Grupo "Leitores" criado com sucesso!'))
        
        # Criar grupo Funcionários
        funcionarios_group, created = Group.objects.get_or_create(name='Funcionários')
        if created:
            # Funcionários têm todas as permissões
            for model in [Livro, Leitor, Funcionario, Emprestimo, Categoria]:
                ct = ContentType.objects.get_for_model(model)
                permissions = Permission.objects.filter(content_type=ct)
                funcionarios_group.permissions.add(*permissions)
            
            self.stdout.write(self.style.SUCCESS('Grupo "Funcionários" criado com sucesso!'))