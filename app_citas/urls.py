from django.urls import path
from . import views

app_name = 'app_citas'

urlpatterns = [
    path('', views.lista_citas, name='lista_citas'),
    path('crear/', views.crear_cita, name='crear_cita'),
]
