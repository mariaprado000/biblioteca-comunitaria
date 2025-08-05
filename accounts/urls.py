from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro_view, name='registro'),
    
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
]