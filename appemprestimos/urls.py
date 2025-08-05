from django.urls import path
from . import views

urlpatterns = [
    # CRUD Empréstimos
    path('', views.emprestimo_list, name='emprestimo_list'),
    path('adicionar/', views.emprestimo_create, name='emprestimo_create'),
    path('<int:pk>/editar/', views.emprestimo_update, name='emprestimo_update'),
    path('<int:pk>/excluir/', views.emprestimo_delete, name='emprestimo_delete'),
    path('<int:pk>/devolver/', views.emprestimo_devolver, name='emprestimo_devolver'),
    path('<int:pk>/renovar/', views.emprestimo_renovar, name='emprestimo_renovar'),
    
    # Relatórios
    path('relatorios/atrasos/', views.relatorio_atrasos, name='relatorio_atrasos'),
]