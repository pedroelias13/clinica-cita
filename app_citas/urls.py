from django.urls import path
from . import views

app_name = 'app_citas'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Citas
    path('citas/', views.lista_citas, name='lista_citas'),
    path('citas/crear/', views.crear_cita, name='crear_cita'),
    path('citas/<int:pk>/editar/', views.editar_cita, name='editar_cita'),
    path('citas/<int:pk>/cancelar/', views.cancelar_cita, name='cancelar_cita'),
    path('citas/historial/', views.historial_citas, name='historial_citas'),
    
    # Doctores
    path('doctores/', views.lista_doctores, name='lista_doctores'),

    # Las siguientes rutas requieren que crees las vistas antes de usarlas:
    # path('citas/<int:pk>/', views.detalle_cita, name='detalle_cita'),
    # path('doctores/<int:pk>/', views.detalle_doctor, name='detalle_doctor'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),

    # Rutas para los dashboards
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('paciente/', views.paciente_dashboard, name='paciente_dashboard'),
]
