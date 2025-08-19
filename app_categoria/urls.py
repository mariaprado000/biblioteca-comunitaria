from django.urls import path
from . import views

app_name = 'app_categoria'

urlpatterns = [
    path('', views.categoria_list, name='listar'),
    path('criar/', views.categoria_create, name='criar'),
    path('<int:pk>/editar/', views.categoria_update, name='editar'),
    path('<int:pk>/deletar/', views.categoria_delete, name='deletar'),
]