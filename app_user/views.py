from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy

class CustomLoginView(auth_views.LoginView):
    template_name = 'app_user/login.html'
    
    def get_success_url(self):
        return reverse_lazy('app_dashboard:home')

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {username}! Agora você pode fazer login.')
            return redirect('app_user:login')
    else:
        form = UserCreationForm()
    return render(request, 'app_user/registro.html', {'form': form})
