from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Cita, Doctor, Paciente, Especialidad, Genero, TipoSangre
from django.utils import timezone
from django.contrib.auth.models import User
from .forms import CitaForm, RegistroForm

@login_required
def lista_citas(request):
    if hasattr(request.user, 'paciente'):
        citas = Cita.objects.filter(paciente=request.user.paciente)
    elif hasattr(request.user, 'doctor'):
        citas = Cita.objects.filter(doctor=request.user.doctor)
    else:
        citas = []
    return render(request, 'app_citas/lista_citas.html', {'citas': citas})

@login_required
def crear_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.paciente = request.user.paciente
            cita.save()
            return redirect('lista_citas')
    else:
        form = CitaForm()
    return render(request, 'app_citas/crear_cita.html', {'form': form})

@login_required
def lista_especialidades(request):
    especialidades = Especialidad.objects.all()
    return render(request, 'app_citas/lista_especialidades.html', {
        'especialidades': especialidades
    })

@login_required
def lista_doctores(request):
    doctores = Doctor.objects.all()
    return render(request, 'app_citas/lista_doctores.html', {
        'doctores': doctores
    })

@login_required
def lista_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'app_citas/lista_pacientes.html', {
        'pacientes': pacientes
    })

@login_required
def dashboard(request):
    context = {
        'total_citas': Cita.objects.count(),
        'mis_citas': Cita.objects.filter(paciente__usuario=request.user) if hasattr(request.user, 'paciente') else Cita.objects.filter(doctor__usuario=request.user)
    }
    return render(request, 'app_citas/dashboard.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('app_citas:dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'registration/login.html')

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            # Crear el paciente asociado
            Paciente.objects.create(
                usuario=user,
                fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
                genero=form.cleaned_data['genero'],
                telefono=form.cleaned_data['telefono'],
                direccion=form.cleaned_data['direccion'],
            )
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})
