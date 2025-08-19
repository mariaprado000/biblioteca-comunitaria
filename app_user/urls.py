from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'app_user'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='app_user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]