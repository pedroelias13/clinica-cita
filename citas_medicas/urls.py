from django.contrib import admin
from django.urls import path, include
<<<<<<< Updated upstream
=======
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
>>>>>>> Stashed changes
from app_citas.views import login_view, registro_view

def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('', redirect_to_login, name='home'),
    path('login/', login_view, name='login'),
    path('registro/', registro_view, name='registro'),
<<<<<<< Updated upstream
=======
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('admin/', admin.site.urls),
>>>>>>> Stashed changes
    path('dashboard/', include('app_citas.urls')),
]
