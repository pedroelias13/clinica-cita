from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from app_citas.views import login_view, registro_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('registro/', registro_view, name='registro'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', include('app_citas.urls')),
]
