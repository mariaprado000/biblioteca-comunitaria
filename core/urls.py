# core/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro_view, name='registro'),
    
    # CRUD Livros
    path('livros/', views.livro_list, name='livro_list'),
    path('livros/adicionar/', views.livro_create, name='livro_create'),
    path('livros/<int:pk>/editar/', views.livro_update, name='livro_update'),
    path('livros/<int:pk>/excluir/', views.livro_delete, name='livro_delete'),
    
    # CRUD Leitores
    path('leitores/', views.leitor_list, name='leitor_list'),
    path('leitores/adicionar/', views.leitor_create, name='leitor_create'),
    path('leitores/meu-cadastro/', views.leitor_create_self, name='leitor_create_self'),
    path('leitores/<int:pk>/editar/', views.leitor_update, name='leitor_update'),
    path('leitores/<int:pk>/excluir/', views.leitor_delete, name='leitor_delete'),
    
    # CRUD Funcionários
    path('funcionarios/', views.funcionario_list, name='funcionario_list'),
    path('funcionarios/adicionar/', views.funcionario_create, name='funcionario_create'),
    path('funcionarios/<int:pk>/editar/', views.funcionario_update, name='funcionario_update'),
    path('funcionarios/<int:pk>/excluir/', views.funcionario_delete, name='funcionario_delete'),
    
    # CRUD Empréstimos
    path('emprestimos/', views.emprestimo_list, name='emprestimo_list'),
    path('emprestimos/adicionar/', views.emprestimo_create, name='emprestimo_create'),
    path('emprestimos/<int:pk>/editar/', views.emprestimo_update, name='emprestimo_update'),
    path('emprestimos/<int:pk>/excluir/', views.emprestimo_delete, name='emprestimo_delete'),
    path('emprestimos/<int:pk>/devolver/', views.emprestimo_devolver, name='emprestimo_devolver'),
    path('emprestimos/<int:pk>/renovar/', views.emprestimo_renovar, name='emprestimo_renovar'),
    
    # CRUD Categorias
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/adicionar/', views.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.categoria_update, name='categoria_update'),
    path('categorias/<int:pk>/excluir/', views.categoria_delete, name='categoria_delete'),
    
    # Relatórios
    path('relatorios/livros-populares/', views.relatorio_livros_populares, name='relatorio_livros_populares'),
    path('relatorios/atrasos/', views.relatorio_atrasos, name='relatorio_atrasos'),
]