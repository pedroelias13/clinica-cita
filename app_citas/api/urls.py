from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
    path('doctores/', views.doctor_list, name='doctor_list'),
    path('citas/<int:pk>/actualizar-estado/', views.actualizar_estado_cita, name='actualizar_estado_cita'),
    path('validar-disponibilidad/', views.validar_disponibilidad, name='validar_disponibilidad'),
]
