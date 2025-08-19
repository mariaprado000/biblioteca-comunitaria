from django.urls import path
from . import views

app_name = 'app_leitor'

urlpatterns = [
    path('', views.leitor_list, name='listar'),
    path('criar/', views.leitor_create, name='criar'),
    path('<int:pk>/editar/', views.leitor_update, name='editar'),
    path('<int:pk>/deletar/', views.leitor_delete, name='deletar'),
]