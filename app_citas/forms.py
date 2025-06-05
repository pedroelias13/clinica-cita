from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Genero, Cita

class RegistroForm(UserCreationForm):
    first_name = forms.CharField(label="Nombre", max_length=30)
    last_name = forms.CharField(label="Apellido", max_length=30)
    email = forms.EmailField(label="Correo electrónico")
    fecha_nacimiento = forms.DateField(
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    genero = forms.ModelChoiceField(
        label="Género",
        queryset=Genero.objects.filter(activo=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    telefono = forms.CharField(
        label="Teléfono",
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Teléfono', 'class': 'form-control'})
    )
    direccion = forms.CharField(
        label="Dirección",
        widget=forms.TextInput(attrs={
            'placeholder': 'Dirección',
            'class': 'form-control',
            'maxlength': 255
        }),
        max_length=255
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}),
        }

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['doctor', 'fecha', 'hora', 'motivo']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
