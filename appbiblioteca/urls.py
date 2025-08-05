from django.urls import path
from . import views

urlpatterns = [
    # CRUD Livros
    path('livros/', views.livro_list, name='livro_list'),
    path('livros/adicionar/', views.livro_create, name='livro_create'),
    path('livros/<int:pk>/editar/', views.livro_update, name='livro_update'),
    path('livros/<int:pk>/excluir/', views.livro_delete, name='livro_delete'),
    
    # CRUD Categorias
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/adicionar/', views.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.categoria_update, name='categoria_update'),
    path('categorias/<int:pk>/excluir/', views.categoria_delete, name='categoria_delete'),
]