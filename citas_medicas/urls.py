from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from app_citas.views import login_view, registro_view
from django.conf import settings
from django.conf.urls.static import static

def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_login, name='home'),
    path('login/', login_view, name='login'),
    path('registro/', registro_view, name='registro'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', include('app_citas.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
