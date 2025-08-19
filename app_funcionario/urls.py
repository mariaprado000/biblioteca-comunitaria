from django.urls import path
from . import views

app_name = 'app_funcionario'

urlpatterns = [
    path('', views.funcionario_list, name='list'),
    path('criar/', views.funcionario_create, name='create'),
    path('<int:pk>/editar/', views.funcionario_update, name='update'),
    path('<int:pk>/deletar/', views.funcionario_delete, name='delete'),
]