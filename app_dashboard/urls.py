from django.urls import path
from . import views

app_name = 'app_dashboard'

urlpatterns = [
    path('', views.home, name='home'),
]