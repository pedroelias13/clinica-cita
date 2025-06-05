from django.urls import path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = 'app_citas'

schema_view = get_schema_view(
    openapi.Info(
        title="MediCitas API",
        default_version='v1',
        description="Documentación de la API de MediCitas",
        contact=openapi.Contact(email="contact@medicitas.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', views.lista_citas, name='lista_citas'),
    path('crear/', views.crear_cita, name='crear_cita'),
    path('especialidades/', views.lista_especialidades, name='lista_especialidades'),
    path('doctores/', views.lista_doctores, name='lista_doctores'),
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('paciente/', views.paciente_dashboard, name='paciente_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
]
