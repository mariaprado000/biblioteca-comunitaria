from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # URLs da nova estrutura
    path('', include('app_dashboard.urls')),  # Dashboard principal
    path('auth/', include('app_user.urls')),  # Autenticação
    path('leitores/', include('app_leitor.urls')),  # Leitores
    path('funcionarios/', include('app_funcionario.urls')),  # Funcionários
    path('livros/', include('app_livro.urls')),  # Livros
    path('categorias/', include('app_categoria.urls')),  # Categorias
    path('emprestimos/', include('app_emprestimo.urls')),  # Empréstimos
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)