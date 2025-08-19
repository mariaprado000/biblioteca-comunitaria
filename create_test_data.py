#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca.settings')
django.setup()

from django.contrib.auth.models import User
from app_categoria.models import Categoria
from app_livro.models import Livro
from app_leitor.models import Leitor
from app_funcionario.models import Funcionario
from app_emprestimo.models import Emprestimo
from datetime import date, timedelta
from django.utils import timezone

def create_test_data():
    print("Criando dados de teste...")
    
    # 1. Criar categorias
    categorias_data = [
        {"nome": "Ficção", "descricao": "Livros de ficção em geral"},
        {"nome": "Romance", "descricao": "Livros românticos"},
        {"nome": "Técnico", "descricao": "Livros técnicos e de programação"},
        {"nome": "História", "descricao": "Livros de história"},
        {"nome": "Infantil", "descricao": "Livros para crianças"},
    ]
    
    for cat_data in categorias_data:
        categoria, created = Categoria.objects.get_or_create(
            nome=cat_data["nome"],
            defaults=cat_data
        )
        if created:
            print(f"Categoria criada: {categoria.nome}")
    
    # 2. Criar livros
    ficcao = Categoria.objects.get(nome="Ficção")
    romance = Categoria.objects.get(nome="Romance")
    tecnico = Categoria.objects.get(nome="Técnico")
    
    livros_data = [
        {"titulo": "1984", "autor": "George Orwell", "ano": 1949, "genero": "Distopia", "categoria": ficcao},
        {"titulo": "Dom Casmurro", "autor": "Machado de Assis", "ano": 1899, "genero": "Romance", "categoria": romance},
        {"titulo": "Python Fluente", "autor": "Luciano Ramalho", "ano": 2015, "genero": "Programação", "categoria": tecnico},
        {"titulo": "O Senhor dos Anéis", "autor": "J.R.R. Tolkien", "ano": 1954, "genero": "Fantasia", "categoria": ficcao},
        {"titulo": "Clean Code", "autor": "Robert Martin", "ano": 2008, "genero": "Programação", "categoria": tecnico},
        {"titulo": "O Cortiço", "autor": "Aluísio Azevedo", "ano": 1890, "genero": "Naturalismo", "categoria": romance},
    ]
    
    for livro_data in livros_data:
        livro, created = Livro.objects.get_or_create(
            titulo=livro_data["titulo"],
            defaults=livro_data
        )
        if created:
            print(f"- Livro criado: {livro.titulo}")
    
    # 3. Criar funcionário admin se não existir
    try:
        admin_user = User.objects.get(username='admin')
        funcionario, created = Funcionario.objects.get_or_create(
            usuario=admin_user,
            defaults={
                'cargo': 'Bibliotecário Chefe',
                'salario': 5000.00,
                'data_admissao': date.today()
            }
        )
        if created:
            print(f"- Funcionário criado: {funcionario}")
    except User.DoesNotExist:
        print("ERRO: Usuário admin não encontrado")
    
    # 4. Criar usuários leitores
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
        }
    ]
    
    for leitor_data in leitores_data:
        user, created = User.objects.get_or_create(
            username=leitor_data["username"],
            defaults={
                "email": leitor_data["email"],
                "first_name": leitor_data["first_name"],
                "last_name": leitor_data["last_name"],
                "password": "pbkdf2_sha256$390000$YourHashedPasswordHere"  # senha: 123456
            }
        )
        user.set_password('123456')  # Senha simples para teste
        user.save()
        
        if created:
            leitor, created2 = Leitor.objects.get_or_create(
                usuario=user,
                defaults={
                    "cpf": leitor_data["cpf"],
                    "telefone": leitor_data["telefone"],
                    "endereco": leitor_data["endereco"],
                    "data_nascimento": leitor_data["data_nascimento"]
                }
            )
            if created2:
                print(f"- Leitor criado: {leitor}")
    
    print(" Dados de teste criados com sucesso!")
    print("\n SISTEMA DE BIBLIOTECA COMUNITÁRIA - PRONTO PARA TESTE!")
    print("\n CREDENCIAIS DE ACESSO:")
    print("FUNCIONARIO FUNCIONÁRIO (admin): username=admin, password=admin123")
    print("LEITORES LEITORES:")
    print("   • username=joao.silva, password=123456")
    print("   • username=maria.prado, password=123456") 
    print("   • username=pedro.oliveira, password=123456")
    print("\nACESSE: Acesse: http://localhost:8000/auth/login/")

if __name__ == "__main__":
    create_test_data()