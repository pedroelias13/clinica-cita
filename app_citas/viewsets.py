from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['especialidad_principal', 'activo']
    search_fields = ['usuario__first_name', 'usuario__last_name']

    @action(detail=True, methods=['get'])
    def citas_hoy(self, request, pk=None):
        doctor = self.get_object()
        citas = doctor.cita_set.filter(fecha=timezone.now().date())
        serializer = CitaSerializer(citas, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def disponibilidad(self, request, pk=None):
        doctor = self.get_object()
        fecha = request.query_params.get('fecha', timezone.now().date())
        return Response(doctor.get_horarios_disponibles(fecha))

    @action(detail=True)
    def estadisticas(self, request, pk=None):
        doctor = self.get_object()
        return Response({
            'total_citas': doctor.cita_set.count(),
            'citas_pendientes': doctor.cita_set.filter(estado='PENDIENTE').count(),
            'pacientes_atendidos': doctor.cita_set.filter(estado='COMPLETADA').count(),
        })

class CitaViewSet(viewsets.ModelViewSet):
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['estado', 'fecha', 'tipo_cita']
    search_fields = ['paciente__usuario__username', 'motivo']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'doctor'):
            return Cita.objects.filter(doctor=user.doctor)
        elif hasattr(user, 'paciente'):
            return Cita.objects.filter(paciente=user.paciente)
        return Cita.objects.none()

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        cita = self.get_object()
        cita.estado = 'CANCELADA'
        cita.save()
        return Response({'status': 'cita cancelada'})

    @action(detail=True, methods=['post'])
    def confirmar(self, request, pk=None):
        cita = self.get_object()
        cita.estado = 'CONFIRMADA'
        cita.save()
        return Response({'status': 'cita confirmada'})
