from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from datetime import date, timedelta
from django.utils import timezone

from accounts.models import Leitor, Funcionario
from appbiblioteca.models import Livro, Categoria
from appemprestimos.models import Emprestimo

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de teste'

    def handle(self, *args, **kwargs):
        self.stdout.write('Criando grupos...')
        # Criar grupos
        grupo_leitores, _ = Group.objects.get_or_create(name='Leitores')
        grupo_funcionarios, _ = Group.objects.get_or_create(name='Funcionários')
        
        self.stdout.write('Criando categorias...')
        # Criar categorias
        categorias = [
            {'nome': 'Ficção', 'descricao': 'Livros de ficção e fantasia'},
            {'nome': 'Romance', 'descricao': 'Livros românticos'},
            {'nome': 'Técnico', 'descricao': 'Livros técnicos e educacionais'},
            {'nome': 'Biografia', 'descricao': 'Biografias e histórias reais'},
            {'nome': 'Autoajuda', 'descricao': 'Livros de desenvolvimento pessoal'},
        ]
        
        for cat_data in categorias:
            Categoria.objects.get_or_create(**cat_data)
        
        self.stdout.write('Criando funcionários...')
        # Criar funcionários
        funcionarios_data = [
            {
                'username': 'func_maria',
                'first_name': 'Maria',
                'last_name': 'Silva',
                'email': 'maria@biblioteca.com',
                'cargo': 'Bibliotecária',
                'salario': 3500.00,
                'data_admissao': date(2020, 1, 15)
            },
            {
                'username': 'func_joao',
                'first_name': 'João',
                'last_name': 'Santos',
                'email': 'joao@biblioteca.com',
                'cargo': 'Auxiliar',
                'salario': 2500.00,
                'data_admissao': date(2021, 6, 1)
            }
        ]
        
        for func_data in funcionarios_data:
            user_data = {k: v for k, v in func_data.items() if k in ['username', 'first_name', 'last_name', 'email']}
            func_model_data = {k: v for k, v in func_data.items() if k in ['cargo', 'salario', 'data_admissao']}
            
            user, created = User.objects.get_or_create(username=user_data['username'], defaults=user_data)
            if created:
                user.set_password('senha123')
                user.is_staff = True
                user.groups.add(grupo_funcionarios)
                user.save()
                
                Funcionario.objects.create(usuario=user, **func_model_data)
        
        self.stdout.write('Criando leitores...')
        # Criar leitores
        leitores_data = [
            {
                'username': '12345678901',
                'first_name': 'Ana',
                'last_name': 'Costa',
                'email': 'ana@email.com',
                'cpf': '12345678901',
                'telefone': '(31) 98765-4321',
                'endereco': 'Rua A, 123',
                'data_nascimento': date(1995, 3, 15)
            },
            {
                'username': '98765432109',
                'first_name': 'Carlos',
                'last_name': 'Oliveira',
                'email': 'carlos@email.com',
                'cpf': '98765432109',
                'telefone': '(31) 91234-5678',
                'endereco': 'Rua B, 456',
                'data_nascimento': date(1988, 7, 22)
            },
            {
                'username': '55566677788',
                'first_name': 'Paula',
                'last_name': 'Rodrigues',
                'email': 'paula@email.com',
                'cpf': '55566677788',
                'telefone': '(31) 99999-8888',
                'endereco': 'Rua C, 789',
                'data_nascimento': date(2000, 11, 5)
            }
        ]
        
        for leitor_data in leitores_data:
            user_data = {k: v for k, v in leitor_data.items() if k in ['username', 'first_name', 'last_name', 'email']}
            leitor_model_data = {k: v for k, v in leitor_data.items() if k in ['cpf', 'telefone', 'endereco', 'data_nascimento']}
            
            user, created = User.objects.get_or_create(username=user_data['username'], defaults=user_data)
            if created:
                user.set_password('senha123')
                user.groups.add(grupo_leitores)
                user.save()
                
                Leitor.objects.create(usuario=user, **leitor_model_data)
        
        self.stdout.write('Criando livros...')
        # Criar livros
        cat_ficcao = Categoria.objects.get(nome='Ficção')
        cat_romance = Categoria.objects.get(nome='Romance')
        cat_tecnico = Categoria.objects.get(nome='Técnico')
        cat_biografia = Categoria.objects.get(nome='Biografia')
        cat_autoajuda = Categoria.objects.get(nome='Autoajuda')
        
        livros_data = [
            {
                'titulo': '1984',
                'autor': 'George Orwell',
                'ano': 1949,
                'genero': 'Ficção Científica',
                'categoria': cat_ficcao,
                'isbn': '9788535914849',
                'editora': 'Companhia das Letras',
                'disponivel': True
            },
            {
                'titulo': 'Dom Casmurro',
                'autor': 'Machado de Assis',
                'ano': 1899,
                'genero': 'Romance',
                'categoria': cat_romance,
                'isbn': '9788520926574',
                'editora': 'Penguin',
                'disponivel': True
            },
            {
                'titulo': 'Python para Iniciantes',
                'autor': 'João Silva',
                'ano': 2023,
                'genero': 'Programação',
                'categoria': cat_tecnico,
                'isbn': '9781234567890',
                'editora': 'Tech Books',
                'disponivel': False
            },
            {
                'titulo': 'Steve Jobs',
                'autor': 'Walter Isaacson',
                'ano': 2011,
                'genero': 'Biografia',
                'categoria': cat_biografia,
                'isbn': '9788535919714',
                'editora': 'Companhia das Letras',
                'disponivel': True
            },
            {
                'titulo': 'O Poder do Hábito',
                'autor': 'Charles Duhigg',
                'ano': 2012,
                'genero': 'Autoajuda',
                'categoria': cat_autoajuda,
                'isbn': '9788539004119',
                'editora': 'Objetiva',
                'disponivel': True
            },
            {
                'titulo': 'Harry Potter e a Pedra Filosofal',
                'autor': 'J.K. Rowling',
                'ano': 1997,
                'genero': 'Fantasia',
                'categoria': cat_ficcao,
                'isbn': '9788532523051',
                'editora': 'Rocco',
                'disponivel': False
            }
        ]
        
        for livro_data in livros_data:
            Livro.objects.get_or_create(titulo=livro_data['titulo'], defaults=livro_data)
        
        self.stdout.write('Criando empréstimos...')
        # Criar empréstimos
        ana = Leitor.objects.get(cpf='12345678901')
        carlos = Leitor.objects.get(cpf='98765432109')
        paula = Leitor.objects.get(cpf='55566677788')
        maria = Funcionario.objects.get(usuario__username='func_maria')
        
        livro_python = Livro.objects.get(titulo='Python para Iniciantes')
        livro_harry = Livro.objects.get(titulo='Harry Potter e a Pedra Filosofal')
        livro_1984 = Livro.objects.get(titulo='1984')
        
        # Empréstimo em andamento
        Emprestimo.objects.get_or_create(
            livro=livro_python,
            leitor=ana,
            funcionario=maria,
            data_devolucao_prevista=timezone.now().date() + timedelta(days=7)
        )
        
        # Empréstimo em atraso
        emp_atraso = Emprestimo.objects.get_or_create(
            livro=livro_harry,
            leitor=carlos,
            funcionario=maria,
            data_devolucao_prevista=timezone.now().date() - timedelta(days=5)
        )[0]
        emp_atraso.data_emprestimo = timezone.now() - timedelta(days=20)
        emp_atraso.save()
        
        # Empréstimo devolvido
        emp_devolvido = Emprestimo.objects.get_or_create(
            livro=livro_1984,
            leitor=paula,
            funcionario=maria,
            data_devolucao_prevista=timezone.now().date() - timedelta(days=10),
            data_devolucao=timezone.now().date() - timedelta(days=12)
        )[0]
        emp_devolvido.data_emprestimo = timezone.now() - timedelta(days=25)
        emp_devolvido.save()
        # Tornar o livro disponível novamente
        livro_1984.disponivel = True
        livro_1984.save()
        
        self.stdout.write(self.style.SUCCESS('Banco de dados populado com sucesso!'))
        self.stdout.write('Usuários criados:')
        self.stdout.write('- Funcionários: func_maria, func_joao (senha: senha123)')
        self.stdout.write('- Leitores: 12345678901, 98765432109, 55566677788 (senha: senha123)')
        self.stdout.write('- Admin: criar manualmente com python manage.py createsuperuser')


