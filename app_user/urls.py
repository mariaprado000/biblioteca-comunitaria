from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'app_user'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
]