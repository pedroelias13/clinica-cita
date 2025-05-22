from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from django.urls import reverse
from .models import (
    Especialidad, Doctor, Paciente, Cita, Diagnostico,

    Receta, Medicamento, Configuracion, NotificacionTemplate,
    SignosVitales, HistorialMedico
)

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'especialidad_principal', 'numero_colegiado', 'activo', 'total_citas')
    list_filter = ('especialidad_principal', 'activo')
    search_fields = ('usuario__username', 'usuario__first_name', 'numero_colegiado')
    filter_horizontal = ('especialidades_adicionales',)
    actions = ['activar_doctores', 'desactivar_doctores']
    
    def total_citas(self, obj):
        return obj.cita_set.count()
    total_citas.short_description = 'Total Citas'

    def activar_doctores(self, request, queryset):
        queryset.update(activo=True)
    activar_doctores.short_description = "Activar doctores seleccionados"

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefono', 'fecha_nacimiento')
    search_fields = ('usuario__username', 'usuario__first_name', 'telefono')

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'doctor', 'fecha', 'hora', 'estado', 'prioridad', 'ver_detalles')
    list_filter = ('estado', 'fecha', 'doctor__especialidad_principal')
    search_fields = ('paciente__usuario__username', 'doctor__usuario__username')
    date_hierarchy = 'fecha'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información Básica', {
            'fields': ('paciente', 'doctor', 'fecha', 'hora', 'estado')
        }),
        ('Detalles de la Cita', {
            'fields': ('motivo', 'tipo_cita', 'prioridad', 'canal_cita', 'link_virtual')
        }),
        ('Información Médica', {
            'fields': ('sintomas', 'info_diagnostico', 'info_receta', 'observaciones')
        }),
        ('Información del Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['marcar_completada', 'marcar_cancelada']
    
    def ver_detalles(self, obj):
        url = reverse('admin:app_citas_cita_change', args=[obj.id])
        return format_html('<a class="button" href="{}">Ver Detalles</a>', url)
    ver_detalles.short_description = 'Acciones'

    def marcar_completada(self, request, queryset):
        queryset.update(estado='COMPLETADA')
    marcar_completada.short_description = "Marcar como completadas"

@admin.register(Diagnostico)
class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = ('cita', 'created_at')
    search_fields = ('cita__paciente__usuario__username', 'descripcion')

@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ('cita', 'created_at')
    search_fields = ('cita__paciente__usuario__username',)

@admin.register(Configuracion)
class ConfiguracionAdmin(admin.ModelAdmin):
    list_display = ('nombre_clinica', 'email', 'telefono')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(NotificacionTemplate)
class NotificacionTemplateAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'activo')
    list_filter = ('tipo', 'activo')
    search_fields = ('nombre', 'asunto', 'contenido')
