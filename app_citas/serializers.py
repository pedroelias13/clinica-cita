from rest_framework import serializers
from .models import (
    Especialidad, Doctor, Paciente, Cita, Diagnostico,
    Receta, Medicamento
)
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    class Meta:
        model = Doctor
        fields = '__all__'

class PacienteSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    class Meta:
        model = Paciente
        fields = '__all__'

class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = '__all__'
        depth = 1
