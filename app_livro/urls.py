from django.urls import path
from . import views

app_name = 'app_livro'

urlpatterns = [
    path('', views.livro_list, name='list'),
    path('criar/', views.livro_create, name='create'),
    path('<int:pk>/editar/', views.livro_update, name='update'),
    path('<int:pk>/deletar/', views.livro_delete, name='delete'),
]