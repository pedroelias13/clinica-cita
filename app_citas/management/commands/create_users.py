from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app_citas.models import Doctor, Paciente, Especialidad, Genero
from django.db import transaction

class Command(BaseCommand):
    help = 'Crea usuarios de prueba: admin, doctor y paciente'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                # Obtener o crear especialidad específica
                especialidad = Especialidad.objects.filter(nombre="Medicina General").first()
                if not especialidad:
                    especialidad = Especialidad.objects.create(
                        nombre="Medicina General",
                        descripcion='Medicina General y Familiar'
                    )
                    self.stdout.write(self.style.SUCCESS('Especialidad creada'))

                # Obtener o crear género
                genero, _ = Genero.objects.get_or_create(
                    codigo="M",
                    defaults={'nombre': 'Masculino'}
                )

                # Crear usuario admin si no existe
                admin_user = User.objects.filter(username='admin').first()
                if not admin_user:
                    admin_user = User.objects.create_superuser(
                        username='admin',
                        email='admin@clinica.com',
                        password='admin123',
                        first_name='Admin',
                        last_name='Sistema'
                    )
                    self.stdout.write(self.style.SUCCESS('Usuario admin creado'))

                # Crear usuario doctor si no existe
                doctor_user = User.objects.filter(username='doctor').first()
                if not doctor_user:
                    doctor_user = User.objects.create_user(
                        username='doctor',
                        email='doctor@clinica.com',
                        password='doctor123',
                        first_name='Juan',
                        last_name='Médico'
                    )
                    Doctor.objects.create(
                        usuario=doctor_user,
                        especialidad_principal=especialidad,
                        titulo='Dr.',
                        consultorio='101',
                        horario_inicio='09:00',
                        horario_fin='18:00'
                    )
                    self.stdout.write(self.style.SUCCESS('Usuario doctor creado'))

                # Crear usuario paciente si no existe
                paciente_user = User.objects.filter(username='paciente').first()
                if not paciente_user:
                    paciente_user = User.objects.create_user(
                        username='paciente',
                        email='paciente@mail.com',
                        password='paciente123',
                        first_name='Pedro',
                        last_name='Paciente'
                    )
                    Paciente.objects.create(
                        usuario=paciente_user,
                        fecha_nacimiento='1990-01-01',
                        genero=genero,
                        telefono='1234567890',
                        direccion='Calle Principal 123'
                    )
                    self.stdout.write(self.style.SUCCESS('Usuario paciente creado'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
