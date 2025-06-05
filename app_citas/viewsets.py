from rest_framework import viewsets, filters
from .models import Doctor, Cita
from .serializers import DoctorSerializer, CitaSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['usuario__first_name', 'usuario__last_name', 'especialidad_principal__nombre']
    ordering_fields = ['usuario__first_name', 'usuario__last_name']

class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['paciente__usuario__first_name', 'doctor__usuario__first_name', 'motivo']
    ordering_fields = ['fecha', 'hora']
