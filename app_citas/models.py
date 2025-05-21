from django.db import models
from django.contrib.auth.models import User

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Especialidades"

    def __str__(self):
        return self.nombre

class Doctor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    numero_colegiado = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15)
    horario_inicio = models.TimeField()
    horario_fin = models.TimeField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.usuario.get_full_name()} - {self.especialidad}"

class Paciente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()
    genero = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    numero_documento = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.numero_documento}"

class Cita(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('COMPLETADA', 'Completada'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    observaciones = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['doctor', 'fecha', 'hora']

    def __str__(self):
        return f"Cita: {self.paciente} con {self.doctor} - {self.fecha} {self.hora}"
