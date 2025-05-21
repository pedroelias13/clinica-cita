from django.urls import path
from . import views

app_name = 'app_citas'

urlpatterns = [
    path('', views.lista_citas, name='lista_citas'),
    path('crear/', views.crear_cita, name='crear_cita'),
    path('especialidades/', views.lista_especialidades, name='lista_especialidades'),
    path('doctores/', views.lista_doctores, name='lista_doctores'),
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
]
