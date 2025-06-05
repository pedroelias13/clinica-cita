from django.contrib import admin
from django.urls import path, include
from app_citas.views import login_view, registro_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('registro/', registro_view, name='registro'),
    path('dashboard/', include('app_citas.urls')),
]
