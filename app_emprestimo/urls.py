from django.urls import path
from . import views

app_name = 'app_emprestimo'

urlpatterns = [
    path('', views.emprestimo_list, name='list'),
    path('criar/', views.emprestimo_create, name='create'),
    path('<int:pk>/devolver/', views.emprestimo_devolver, name='devolver'),
    path('<int:pk>/renovar/', views.emprestimo_renovar, name='renovar'),
]