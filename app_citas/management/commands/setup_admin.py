from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    help = 'Configura el usuario asus como administrador'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                # Obtener o crear el usuario asus
                user = User.objects.get(username='asus')
                
                # Asegurar que es superusuario y staff
                if not user.is_superuser or not user.is_staff:
                    user.is_superuser = True
                    user.is_staff = True
                    user.save()
                    self.stdout.write(self.style.SUCCESS('Usuario asus actualizado como administrador'))
                else:
                    self.stdout.write(self.style.SUCCESS('Usuario asus ya es administrador'))
                
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Usuario asus no encontrado'))
