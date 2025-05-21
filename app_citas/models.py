from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

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
        return self.doctor_set.filter(activo=True).count()

class Doctor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    numero_colegiado = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15)
    horario_inicio = models.TimeField()
    horario_fin = models.TimeField()
    duracion_cita = models.IntegerField(default=30, help_text="Duración de cada cita en minutos")
    activo = models.BooleanField(default=True)
    foto = models.ImageField(upload_to='doctores/', null=True, blank=True)
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

class Paciente(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro')
    ]
    
    TIPO_SANGRE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    tipo_sangre = models.CharField(max_length=3, choices=TIPO_SANGRE_CHOICES, null=True, blank=True)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()
    alergias = models.TextField(blank=True)
    antecedentes = models.TextField(blank=True)
    contacto_emergencia = models.CharField(max_length=100, blank=True)
    telefono_emergencia = models.CharField(max_length=15, blank=True)
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
    diagnostico = models.TextField(blank=True)
    receta = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha', '-hora']
        unique_together = ['doctor', 'fecha', 'hora']

    def __str__(self):
        return f"Cita: {self.paciente} con {self.doctor} - {self.fecha} {self.hora}"

    def clean(self):
        # Validar que la hora esté dentro del horario del doctor
        if self.hora < self.doctor.horario_inicio or self.hora >= self.doctor.horario_fin:
            raise ValidationError('La hora de la cita debe estar dentro del horario del doctor')

        # Validar que la fecha no sea en el pasado
        if self.fecha < datetime.now().date():
            raise ValidationError('No se pueden agendar citas en fechas pasadas')

        # Nuevas validaciones de seguridad
        # Verificar si ya existe una cita en el mismo horario
        citas_mismo_horario = Cita.objects.filter(
            doctor=self.doctor,
            fecha=self.fecha,
            hora=self.hora
        ).exclude(id=self.id)
        
        if citas_mismo_horario.exists():
            raise ValidationError('Ya existe una cita programada para este horario')

        # Verificar que no exceda el límite de citas por día para el paciente
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
