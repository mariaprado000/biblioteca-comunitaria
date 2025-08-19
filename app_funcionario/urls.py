from django.urls import path
from . import views

app_name = 'app_funcionario'

urlpatterns = [
    path('', views.funcionario_list, name='listar'),
    path('criar/', views.funcionario_create, name='criar'),
    path('<int:pk>/editar/', views.funcionario_update, name='editar'),
    path('<int:pk>/deletar/', views.funcionario_delete, name='deletar'),
]