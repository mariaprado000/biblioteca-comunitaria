from django.urls import path
from . import views

app_name = 'app_categoria'

urlpatterns = [
    path('', views.categoria_list, name='list'),
    path('criar/', views.categoria_create, name='create'),
    path('<int:pk>/editar/', views.categoria_update, name='update'),
    path('<int:pk>/deletar/', views.categoria_delete, name='delete'),
]