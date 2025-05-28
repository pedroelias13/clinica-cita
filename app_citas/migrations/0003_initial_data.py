from django.db import migrations

def create_initial_data(apps, schema_editor):
    Especialidad = apps.get_model('app_citas', 'Especialidad')
    Genero = apps.get_model('app_citas', 'Genero')
    TipoSangre = apps.get_model('app_citas', 'TipoSangre')

    # Crear especialidades básicas
    especialidades = [
        ('Medicina General', 'Atención médica general'),
        ('Pediatría', 'Atención médica infantil'),
        ('Cardiología', 'Especialista en corazón'),
    ]
    for nombre, desc in especialidades:
        Especialidad.objects.create(nombre=nombre, descripcion=desc)

    # Crear géneros
    for codigo, nombre in [('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]:
        Genero.objects.create(codigo=codigo, nombre=nombre)

    # Crear tipos de sangre
    tipos_sangre = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    for tipo in tipos_sangre:
        TipoSangre.objects.create(codigo=tipo, nombre=tipo)

class Migration(migrations.Migration):
    dependencies = [
        ('app_citas', '0002_configuracion_genero_notificaciontemplate_and_more'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]
