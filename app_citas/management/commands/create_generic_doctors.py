from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app_citas.models import Doctor, Especialidad
from django.db import transaction

class Command(BaseCommand):
    help = 'Crea doctores genéricos con distintas especialidades'

    def handle(self, *args, **kwargs):
        especialidades = [
            ("Medicina General", "fa-stethoscope"),
            ("Pediatría", "fa-child"),
            ("Cardiología", "fa-heartbeat"),
            ("Dermatología", "fa-user-md"),
            ("Ginecología", "fa-female"),
            ("Traumatología", "fa-wheelchair"),
            ("Oftalmología", "fa-eye"),
        ]
        with transaction.atomic():
            for idx, (nombre, icono) in enumerate(especialidades, start=1):
                esp = Especialidad.objects.filter(nombre=nombre).first()
                if not esp:
                    esp = Especialidad.objects.create(
                        nombre=nombre,
                        descripcion=nombre,
                        icono=icono
                    )
                username = f"doctor{idx}"
                if not User.objects.filter(username=username).exists():
                    user = User.objects.create_user(
                        username=username,
                        email=f"{username}@mail.com",
                        password="doctor123",
                        first_name=f"Doctor{idx}",
                        last_name=nombre
                    )
                    Doctor.objects.create(
                        usuario=user,
                        especialidad_principal=esp,
                        titulo="Dr.",
                        consultorio=f"{100+idx}",
                        horario_inicio="08:00",
                        horario_fin="16:00",
                        activo=True
                    )
                    self.stdout.write(self.style.SUCCESS(f"Doctor {username} ({nombre}) creado"))
                else:
                    self.stdout.write(self.style.WARNING(f"Doctor {username} ya existe"))
