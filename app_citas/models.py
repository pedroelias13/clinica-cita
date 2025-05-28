from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta

class Configuracion(models.Model):
    """Configuraciones generales del sistema"""
    nombre_clinica = models.CharField(max_length=200)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    logo = models.ImageField(upload_to='configuracion/', null=True, blank=True)
    citas_por_dia = models.IntegerField(default=3)
    dias_max_agenda = models.IntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuración'
        verbose_name_plural = 'Configuraciones'

class NotificacionTemplate(models.Model):
    """Plantillas para notificaciones"""
    TIPO_CHOICES = [
        ('EMAIL', 'Correo Electrónico'),
        ('SMS', 'Mensaje de Texto'),
        ('WHATSAPP', 'WhatsApp'),
    ]
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    asunto = models.CharField(max_length=200)
    contenido = models.TextField(help_text="Usa {variables} para contenido dinámico")
    activo = models.BooleanField(default=True)

class Notificacion(models.Model):
    """Registro de notificaciones enviadas"""
    template = models.ForeignKey(NotificacionTemplate, on_delete=models.PROTECT)
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE)
    enviado = models.BooleanField(default=False)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    error = models.TextField(blank=True)

class CalificacionCita(models.Model):
    """Evaluaciones de las citas"""
    cita = models.OneToOneField('Cita', on_delete=models.CASCADE)
    puntuacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class RegistroAcciones(models.Model):
    """Registro de acciones importantes en el sistema"""
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=50)
    descripcion = models.TextField()
    modelo_afectado = models.CharField(max_length=50)
    id_registro = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True)

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    icono = models.CharField(max_length=50, help_text="Nombre del ícono de FontAwesome", default="fa-stethoscope")
    color = models.CharField(max_length=20, default="primary")
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Especialidades"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def get_doctores_activos(self):
        return self.doctores_principal.filter(activo=True).count()

class HorarioDoctor(models.Model):
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    dia_semana = models.IntegerField(choices=[
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ])
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ['doctor', 'dia_semana']

    def __str__(self):
        return f"{self.doctor} - {self.get_dia_semana_display()}"

class HistorialMedico(models.Model):
    paciente = models.OneToOneField('Paciente', on_delete=models.CASCADE)
    grupo_sanguineo = models.CharField(max_length=3)
    alergias = models.TextField(blank=True)
    enfermedades_cronicas = models.TextField(blank=True)
    cirugias_previas = models.TextField(blank=True)
    medicamentos_actuales = models.TextField(blank=True)
    antecedentes_familiares = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

class SignosVitales(models.Model):
    cita = models.OneToOneField('Cita', on_delete=models.CASCADE)
    presion_arterial = models.CharField(max_length=20)
    frecuencia_cardiaca = models.IntegerField()
    temperatura = models.DecimalField(max_digits=4, decimal_places=1)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=3, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class Diagnostico(models.Model):
    cita = models.OneToOneField('Cita', on_delete=models.CASCADE, related_name='diagnostico_completo')
    descripcion = models.TextField()
    recomendaciones = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Receta(models.Model):
    cita = models.OneToOneField('Cita', on_delete=models.CASCADE, related_name='receta_medica')
    created_at = models.DateTimeField(auto_now_add=True)
    indicaciones_generales = models.TextField()

class Medicamento(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    dosis = models.CharField(max_length=50)
    frecuencia = models.CharField(max_length=50)
    duracion = models.CharField(max_length=50)
    indicaciones = models.TextField()

class Doctor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    especialidad_principal = models.ForeignKey(
        Especialidad, 
        on_delete=models.CASCADE,
        related_name='doctores_principal',
        default=1  # Asumiendo que 1 será el ID de la primera especialidad
    )
    especialidades_adicionales = models.ManyToManyField(
        Especialidad,
        related_name='doctores_adicionales',
        blank=True
    )
    numero_colegiado = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15)
    horario_inicio = models.TimeField()
    horario_fin = models.TimeField()
    duracion_cita = models.IntegerField(default=30, help_text="Duración de cada cita en minutos")
    activo = models.BooleanField(default=True)
    foto = models.ImageField(upload_to='doctores/', null=True, blank=True)
    consultorio = models.CharField(max_length=50, blank=True)
    titulo = models.CharField(max_length=100, blank=True)
    biografia = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['usuario__first_name', 'usuario__last_name']

    def __str__(self):
        return f"Dr. {self.usuario.get_full_name()}"

    def get_citas_hoy(self):
        return self.cita_set.filter(fecha=datetime.now().date())

    def get_horarios_disponibles(self, fecha):
        # Obtener todas las citas del día
        citas_dia = self.cita_set.filter(fecha=fecha)
        horarios_ocupados = [cita.hora for cita in citas_dia]
        
        # Generar todos los horarios posibles
        horarios_disponibles = []
        hora_actual = datetime.combine(fecha, self.horario_inicio)
        hora_fin = datetime.combine(fecha, self.horario_fin)
        
        while hora_actual < hora_fin:
            if hora_actual.time() not in horarios_ocupados:
                horarios_disponibles.append(hora_actual.time())
            hora_actual += timedelta(minutes=self.duracion_cita)
        
        return horarios_disponibles

class Genero(models.Model):
    codigo = models.CharField(max_length=1, primary_key=True)
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class TipoSangre(models.Model):
    codigo = models.CharField(max_length=3, primary_key=True)
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField(blank=True)
    puede_donar_a = models.ManyToManyField('self', symmetrical=False, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Paciente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField()
    genero = models.ForeignKey(Genero, on_delete=models.PROTECT)
    tipo_sangre = models.ForeignKey(TipoSangre, on_delete=models.PROTECT, null=True, blank=True)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()
    alergias = models.TextField(blank=True)
    antecedentes = models.TextField(blank=True)
    contacto_emergencia = models.CharField(max_length=100, blank=True)
    telefono_emergencia = models.CharField(max_length=15, blank=True)
    ocupacion = models.CharField(max_length=100, blank=True)
    estado_civil = models.CharField(max_length=20, choices=[
        ('S', 'Soltero'),
        ('C', 'Casado'),
        ('D', 'Divorciado'),
        ('V', 'Viudo'),
    ], blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.usuario.get_full_name()

    def get_edad(self):
        today = datetime.now().date()
        return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

class Cita(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('COMPLETADA', 'Completada'),
        ('NO_ASISTIO', 'No Asistió'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    sintomas = models.TextField(blank=True)
    info_diagnostico = models.TextField(blank=True)  # Renombramos diagnostico
    info_receta = models.TextField(blank=True)      # Renombramos receta
    observaciones = models.TextField(blank=True)
    tipo_cita = models.CharField(max_length=20, choices=[
        ('PRIMERA_VEZ', 'Primera Vez'),
        ('SEGUIMIENTO', 'Seguimiento'),
        ('CONTROL', 'Control'),
        ('EMERGENCIA', 'Emergencia'),
    ], default='PRIMERA_VEZ')
    prioridad = models.CharField(max_length=20, choices=[
        ('NORMAL', 'Normal'),
        ('URGENTE', 'Urgente'),
        ('EMERGENCIA', 'Emergencia'),
    ], default='NORMAL')
    recordatorio_enviado = models.BooleanField(default=False)
    tiempo_espera = models.IntegerField(null=True, blank=True, help_text="Tiempo de espera en minutos")
    canal_cita = models.CharField(max_length=20, choices=[
        ('PRESENCIAL', 'Presencial'),
        ('VIRTUAL', 'Virtual'),
        ('TELEFONICA', 'Telefónica')
    ], default='PRESENCIAL')
    link_virtual = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha', '-hora']
        unique_together = ['doctor', 'fecha', 'hora']

    def __str__(self):
        return f"Cita: {self.paciente} con {self.doctor} - {self.fecha} {self.hora}"

    def clean(self):
        # Validaciones existentes y nuevas
        if self.hora < self.doctor.horario_inicio or self.hora >= self.doctor.horario_fin:
            raise ValidationError('La hora de la cita debe estar dentro del horario del doctor')

        if self.fecha < datetime.now().date():
            raise ValidationError('No se pueden agendar citas en fechas pasadas')

        # Verificar citas duplicadas
        citas_mismo_horario = Cita.objects.filter(
            doctor=self.doctor,
            fecha=self.fecha,
            hora=self.hora
        ).exclude(id=self.id)
        
        if citas_mismo_horario.exists():
            raise ValidationError('Ya existe una cita programada para este horario')

        # Verificar límite de citas
        citas_paciente_dia = Cita.objects.filter(
            paciente=self.paciente,
            fecha=self.fecha
        ).exclude(estado='CANCELADA').count()
        
        if citas_paciente_dia >= 3:
            raise ValidationError('No se pueden agendar más de 3 citas por día para el mismo paciente')

    def is_modificable(self):
        """Verifica si la cita puede ser modificada"""
        return self.estado in ['PENDIENTE', 'CONFIRMADA'] and \
               self.fecha >= datetime.now().date()

    def validar_disponibilidad(self):
        """Verifica la disponibilidad del doctor en el horario seleccionado"""
        horarios_disponibles = self.doctor.get_horarios_disponibles(self.fecha)
        return self.hora in horarios_disponibles

    def get_estado_color(self):
        return {
            'PENDIENTE': 'warning',
            'CONFIRMADA': 'primary',
            'CANCELADA': 'danger',
            'COMPLETADA': 'success',
            'NO_ASISTIO': 'secondary',
        }.get(self.estado, 'info')

    def enviar_recordatorio(self):
        """Envía recordatorio de cita"""
        if not self.recordatorio_enviado and self.fecha == timezone.now().date() + timezone.timedelta(days=1):
            # Lógica de envío
            self.recordatorio_enviado = True
            self.save()

    def registrar_llegada(self):
        """Registra la llegada del paciente"""
        self.tiempo_espera = 0
        self.save()
        return RegistroAcciones.objects.create(
            usuario=self.paciente.usuario,
            accion='LLEGADA_PACIENTE',
            descripcion=f'Paciente llegó a su cita con {self.doctor}',
            modelo_afectado='Cita',
            id_registro=self.id
        )
