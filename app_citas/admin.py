from django.contrib import admin
from .models import Especialidad, Doctor, Paciente, Cita

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'especialidad', 'numero_colegiado', 'activo')
    list_filter = ('especialidad', 'activo')
    search_fields = ('usuario__username', 'usuario__first_name', 'numero_colegiado')

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'numero_documento', 'telefono')
    search_fields = ('usuario__username', 'numero_documento')

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'doctor', 'fecha', 'hora', 'estado')
    list_filter = ('estado', 'fecha', 'doctor__especialidad')
    search_fields = ('paciente__usuario__username', 'doctor__usuario__username')
    date_hierarchy = 'fecha'
