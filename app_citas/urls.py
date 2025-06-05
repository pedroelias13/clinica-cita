from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import DoctorViewSet, CitaViewSet
from . import views

router = DefaultRouter()
router.register(r'doctores', DoctorViewSet)
router.register(r'citas', CitaViewSet, basename='cita')

app_name = 'app_citas'

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.dashboard, name='dashboard'),
    path('citas/', views.lista_citas, name='lista_citas'),
    path('crear/', views.crear_cita, name='crear_cita'),
    path('especialidades/', views.lista_especialidades, name='lista_especialidades'),
    path('doctores/', views.lista_doctores, name='lista_doctores'),
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    # Agrega aquí más rutas si tienes más plantillas/vistas
]
