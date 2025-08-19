from django.urls import path
from . import views

app_name = 'app_livro'

urlpatterns = [
    path('', views.livro_list, name='listar'),
    path('criar/', views.livro_create, name='criar'),
    path('<int:pk>/editar/', views.livro_update, name='editar'),
    path('<int:pk>/deletar/', views.livro_delete, name='deletar'),
]