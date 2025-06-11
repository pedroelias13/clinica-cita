from django.contrib import admin
from django.urls import path, include
from app_citas.views import login_view, registro_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('registro/', registro_view, name='registro'),
    path('citas/', include('app_citas.urls')),
    path('api/', include('app_citas.api.urls')),  # Agregar rutas API
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
