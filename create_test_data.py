#!/usr/bin/env python
"""
Script para criar dados de teste completos para o Sistema de Biblioteca Comunitária.

Este script configura:
- Grupos e permissões necessárias
- Usuário administrativo
- Dados de exemplo (categorias, livros, usuários)

Execute com: python create_test_data.py
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from app_categoria.models import Categoria
from app_livro.models import Livro
from app_leitor.models import Leitor
from app_funcionario.models import Funcionario
from app_emprestimo.models import Emprestimo
from datetime import date, timedelta
from django.utils import timezone

def create_groups_and_permissions():
    """Criar grupos e configurar permissões"""
    print("* Configurando grupos e permissoes...")
    
    # Criar grupo de Funcionários
    funcionarios_group, created = Group.objects.get_or_create(name='Funcionarios')
    if created:
        print("   + Grupo 'Funcionarios' criado")
    
    # Criar grupo de Leitores
    leitores_group, created = Group.objects.get_or_create(name='Leitores')
    if created:
        print("   + Grupo 'Leitores' criado")
    
    # Configurar permissões para Funcionários (acesso total)
    funcionario_permissions = [
        'add_categoria', 'change_categoria', 'delete_categoria', 'view_categoria',
        'add_livro', 'change_livro', 'delete_livro', 'view_livro',
        'add_leitor', 'change_leitor', 'delete_leitor', 'view_leitor',
        'add_funcionario', 'change_funcionario', 'delete_funcionario', 'view_funcionario',
        'add_emprestimo', 'change_emprestimo', 'delete_emprestimo', 'view_emprestimo',
    ]
    
    for perm_codename in funcionario_permissions:
        try:
            permission = Permission.objects.get(codename=perm_codename)
            funcionarios_group.permissions.add(permission)
        except Permission.DoesNotExist:
            print(f"   ! Permissao '{perm_codename}' nao encontrada")
    
    # Configurar permissões para Leitores (acesso limitado)
    leitor_permissions = [
        'view_categoria',
        'view_livro',
        'view_emprestimo',
    ]
    
    for perm_codename in leitor_permissions:
        try:
            permission = Permission.objects.get(codename=perm_codename)
            leitores_group.permissions.add(permission)
        except Permission.DoesNotExist:
            print(f"   ! Permissao '{perm_codename}' nao encontrada")
    
    print("   + Permissoes configuradas")
    return funcionarios_group, leitores_group

def create_admin_user(funcionarios_group):
    """Criar usuário administrativo"""
    print("* Criando usuario administrativo...")
    
    # Criar superusuário admin
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@biblioteca.com',
            'first_name': 'Administrador',
            'last_name': 'Sistema',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        }
    )
    
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("   + Usuario admin criado (username: admin, password: admin123)")
    else:
        # Garantir que a senha esteja correta
        admin_user.set_password('admin123')
        admin_user.save()
        print("   + Usuario admin ja existe (senha redefinida para admin123)")
    
    # Adicionar ao grupo de funcionários
    admin_user.groups.add(funcionarios_group)
    
    # Criar perfil de funcionário para o admin
    funcionario, created = Funcionario.objects.get_or_create(
        usuario=admin_user,
        defaults={
            'cargo': 'Bibliotecario Chefe',
            'salario': 5000.00,
            'data_admissao': date.today(),
            'ativo': True
        }
    )
    
    if created:
        print("   + Perfil de funcionario criado para admin")
    
    return admin_user

def create_test_data():
    print("INICIANDO CONFIGURACAO DO SISTEMA DE BIBLIOTECA COMUNITARIA")
    print("=" * 60)
    
    # 1. Criar grupos e permissões
    funcionarios_group, leitores_group = create_groups_and_permissions()
    
    # 2. Criar usuário admin
    admin_user = create_admin_user(funcionarios_group)
    
    # 3. Criar categorias
    print("* Criando categorias...")
    categorias_data = [
        {"nome": "Ficção", "descricao": "Livros de ficção em geral"},
        {"nome": "Romance", "descricao": "Livros românticos"},
        {"nome": "Técnico", "descricao": "Livros técnicos e de programação"},
        {"nome": "História", "descricao": "Livros de história"},
        {"nome": "Infantil", "descricao": "Livros para crianças"},
        {"nome": "Ciências", "descricao": "Livros científicos"},
        {"nome": "Biografia", "descricao": "Biografias e memórias"},
    ]
    
    for cat_data in categorias_data:
        categoria, created = Categoria.objects.get_or_create(
            nome=cat_data["nome"],
            defaults=cat_data
        )
        if created:
            print(f"   + Categoria criada: {categoria.nome}")
    
    # 4. Criar livros
    print("* Criando livros de exemplo...")
    ficcao = Categoria.objects.get(nome="Ficção")
    romance = Categoria.objects.get(nome="Romance")
    tecnico = Categoria.objects.get(nome="Técnico")
    historia = Categoria.objects.get(nome="História")
    infantil = Categoria.objects.get(nome="Infantil")
    
    livros_data = [
        {"titulo": "1984", "autor": "George Orwell", "ano": 1949, "genero": "Distopia", "categoria": ficcao, "isbn": "9780451524935", "editora": "Penguin Books"},
        {"titulo": "Dom Casmurro", "autor": "Machado de Assis", "ano": 1899, "genero": "Romance", "categoria": romance, "isbn": "9788525412065", "editora": "Globo"},
        {"titulo": "Python Fluente", "autor": "Luciano Ramalho", "ano": 2015, "genero": "Programação", "categoria": tecnico, "isbn": "9788575224625", "editora": "Novatec"},
        {"titulo": "O Senhor dos Anéis", "autor": "J.R.R. Tolkien", "ano": 1954, "genero": "Fantasia", "categoria": ficcao, "isbn": "9780547928227", "editora": "Houghton Mifflin"},
        {"titulo": "Clean Code", "autor": "Robert Martin", "ano": 2008, "genero": "Programação", "categoria": tecnico, "isbn": "9780132350884", "editora": "Prentice Hall"},
        {"titulo": "O Cortiço", "autor": "Aluísio Azevedo", "ano": 1890, "genero": "Naturalismo", "categoria": romance, "isbn": "9788508133000", "editora": "Ática"},
        {"titulo": "História do Brasil", "autor": "Boris Fausto", "ano": 2006, "genero": "História", "categoria": historia, "isbn": "9788531410260", "editora": "Edusp"},
        {"titulo": "O Pequeno Príncipe", "autor": "Antoine de Saint-Exupéry", "ano": 1943, "genero": "Infantil", "categoria": infantil, "isbn": "9788525412348", "editora": "Globo"},
        {"titulo": "Django for Beginners", "autor": "William Vincent", "ano": 2022, "genero": "Programação", "categoria": tecnico, "isbn": "9781735467207", "editora": "Django Books"},
        {"titulo": "Capitães da Areia", "autor": "Jorge Amado", "ano": 1937, "genero": "Romance", "categoria": romance, "isbn": "9788535909818", "editora": "Companhia das Letras"},
    ]
    
    for livro_data in livros_data:
        livro, created = Livro.objects.get_or_create(
            titulo=livro_data["titulo"],
            defaults=livro_data
        )
        if created:
            print(f"   + Livro criado: {livro.titulo}")
    
    # 5. Criar funcionário adicional
    print("* Criando funcionario de exemplo...")
    funcionario_user, created = User.objects.get_or_create(
        username='funcionario1',
        defaults={
            'email': 'funcionario@biblioteca.com',
            'first_name': 'Ana',
            'last_name': 'Santos',
            'is_active': True,
        }
    )
    
    if created:
        funcionario_user.set_password('func123')
        funcionario_user.save()
        funcionario_user.groups.add(funcionarios_group)
        
        funcionario, created2 = Funcionario.objects.get_or_create(
            usuario=funcionario_user,
            defaults={
                'cargo': 'Bibliotecário Assistente',
                'salario': 3000.00,
                'data_admissao': date.today(),
                'ativo': True
            }
        )
        if created2:
            print("   + Funcionário Ana Santos criado")
    
    # 6. Criar usuários leitores
    print("* Criando leitores de exemplo...")
    leitores_data = [
        {
            "username": "joao.silva", "email": "joao@email.com", "first_name": "João", "last_name": "Silva",
            "cpf": "12345678901", "telefone": "(11) 99999-9999", "endereco": "Rua A, 123", "data_nascimento": date(1990, 1, 15)
        },
        {
            "username": "maria.prado", "email": "maria@email.com", "first_name": "Maria", "last_name": "Prado",
            "cpf": "98765432109", "telefone": "(11) 88888-8888", "endereco": "Rua B, 456", "data_nascimento": date(1985, 5, 20)
        },
        {
            "username": "pedro.oliveira", "email": "pedro@email.com", "first_name": "Pedro", "last_name": "Oliveira", 
            "cpf": "11223344556", "telefone": "(11) 77777-7777", "endereco": "Rua C, 789", "data_nascimento": date(1992, 10, 30)
        },
        {
            "username": "ana.costa", "email": "ana@email.com", "first_name": "Ana", "last_name": "Costa",
            "cpf": "55566677788", "telefone": "(11) 66666-6666", "endereco": "Rua D, 321", "data_nascimento": date(1988, 8, 12)
        }
    ]
    
    for leitor_data in leitores_data:
        user, created = User.objects.get_or_create(
            username=leitor_data["username"],
            defaults={
                "email": leitor_data["email"],
                "first_name": leitor_data["first_name"],
                "last_name": leitor_data["last_name"],
                "is_active": True,
            }
        )
        user.set_password('123456')  # Senha simples para teste
        user.save()
        user.groups.add(leitores_group)
        
        # Tentar criar o leitor, mas verificar CPF único
        try:
            leitor, created2 = Leitor.objects.get_or_create(
                cpf=leitor_data["cpf"],
                defaults={
                    "usuario": user,
                    "telefone": leitor_data["telefone"],
                    "endereco": leitor_data["endereco"],
                    "data_nascimento": leitor_data["data_nascimento"],
                    "ativo": True
                }
            )
            if created2:
                print(f"   + Leitor criado: {leitor.usuario.first_name} {leitor.usuario.last_name}")
        except Exception as e:
            print(f"   ! Leitor {leitor_data['first_name']} ja existe ou erro: {e}")
    
    # 7. Criar alguns empréstimos de exemplo
    print("* Criando emprestimos de exemplo...")
    try:
        # Pegar alguns livros e leitores para criar empréstimos
        livro1 = Livro.objects.get(titulo="1984")
        livro2 = Livro.objects.get(titulo="Python Fluente")
        leitor1 = Leitor.objects.get(cpf="12345678901")  # João Silva
        funcionario_admin = Funcionario.objects.get(usuario=admin_user)
        
        # Empréstimo ativo
        emprestimo1, created = Emprestimo.objects.get_or_create(
            livro=livro1,
            leitor=leitor1,
            defaults={
                'emprestado_por': funcionario_admin,
                'data_devolucao_prevista': date.today() + timedelta(days=14),
                'renovacao': None  # Empréstimo original (não é renovação)
            }
        )
        if created:
            livro1.disponivel = False
            livro1.save()
            print(f"   + Empréstimo criado: {livro1.titulo} para {leitor1.usuario.first_name}")
        
    except Exception as e:
        print(f"   !  Erro ao criar empréstimos: {e}")
    
    print("\n" + "=" * 60)
    print("* SISTEMA DE BIBLIOTECA COMUNITARIA CONFIGURADO COM SUCESSO!")
    print("=" * 60)
    print("\nRESUMO:")
    print(f"   - Categorias: {Categoria.objects.count()}")
    print(f"   - Livros: {Livro.objects.count()}")
    print(f"   - Funcionarios: {Funcionario.objects.count()}")
    print(f"   - Leitores: {Leitor.objects.count()}")
    print(f"   - Emprestimos: {Emprestimo.objects.count()}")
    print(f"   - Grupos: {Group.objects.count()}")
    
    print("\nCREDENCIAIS DE ACESSO:")
    print("+" + "-" * 57 + "+")
    print("|                   ADMINISTRADOR                         |")
    print("|  Username: admin                                        |")
    print("|  Password: admin123                                     |")
    print("|  Acesso: Total (CRUD em todas as funcionalidades)      |")
    print("+" + "-" * 57 + "+")
    print("|                   FUNCIONARIO                           |")
    print("|  Username: funcionario1                                 |")
    print("|  Password: func123                                      |")
    print("|  Acesso: Total (CRUD em todas as funcionalidades)      |")
    print("+" + "-" * 57 + "+")
    print("|                   LEITORES                              |")
    print("|  Username: joao.silva     | Password: 123456           |")
    print("|  Username: maria.prado    | Password: 123456           |")
    print("|  Username: pedro.oliveira | Password: 123456           |")
    print("|  Username: ana.costa      | Password: 123456           |")
    print("|  Acesso: Limitado (visualizacao apenas)                |")
    print("+" + "-" * 57 + "+")
    
    print("\nACESSO AO SISTEMA:")
    print("   URL: http://localhost:8000/auth/login/")
    print("   Para iniciar: python manage.py runserver")
    
    print("\nPROXIMOS PASSOS:")
    print("   1. Execute: python manage.py runserver")
    print("   2. Acesse: http://localhost:8000")
    print("   3. Faca login com uma das credenciais acima")
    print("   4. Teste todas as funcionalidades do sistema")
    
    print("\nSistema pronto para uso completo!")
    print("=" * 60)

if __name__ == "__main__":
    create_test_data()