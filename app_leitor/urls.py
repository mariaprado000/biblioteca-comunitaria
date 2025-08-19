from django.urls import path
from . import views

app_name = 'app_leitor'

urlpatterns = [
    path('', views.leitor_list, name='list'),
    path('criar/', views.leitor_create, name='create'),
    path('<int:pk>/editar/', views.leitor_update, name='update'),
    path('<int:pk>/deletar/', views.leitor_delete, name='delete'),
]