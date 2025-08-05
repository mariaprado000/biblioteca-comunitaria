from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('relatorios/livros-populares/', views.relatorio_livros_populares, name='relatorio_livros_populares'),
]