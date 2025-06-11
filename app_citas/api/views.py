from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from ..models import Doctor, Cita
from datetime import datetime

@api_view(['GET'])
def dashboard_stats(request):
    today = timezone.now().date()
    return Response({
        'total_citas': Cita.objects.count(),
        'citas_pendientes': Cita.objects.filter(estado='PENDIENTE').count(),
        'citas_hoy': Cita.objects.filter(fecha=today).count()
    })

@api_view(['GET'])
def doctor_list(request):
    doctores = Doctor.objects.filter(activo=True)
    return Response([{
        'id': doctor.id,
        'nombre': doctor.usuario.get_full_name(),
        'especialidad': doctor.especialidad_principal.nombre
    } for doctor in doctores])

@api_view(['POST'])
def actualizar_estado_cita(request, pk):
    try:
        cita = Cita.objects.get(pk=pk)
        cita.estado = request.data.get('estado', 'COMPLETADA')
        cita.save()
        return Response({'success': True})
    except Cita.DoesNotExist:
        return Response({'success': False}, status=404)

@api_view(['GET'])
def validar_disponibilidad(request):
    doctor_id = request.GET.get('doctor')
    fecha = request.GET.get('fecha')
    hora = request.GET.get('hora')
    if not (doctor_id and fecha and hora):
        return Response({'disponible': False, 'error': 'Datos incompletos'}, status=400)
    try:
        doctor = Doctor.objects.get(pk=doctor_id)
        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()
        hora_dt = datetime.strptime(hora, "%H:%M").time()
        existe = Cita.objects.filter(doctor=doctor, fecha=fecha_dt, hora=hora_dt, estado__in=['PENDIENTE', 'CONFIRMADA']).exists()
        return Response({'disponible': not existe})
    except Exception as e:
        return Response({'disponible': False, 'error': str(e)}, status=400)
