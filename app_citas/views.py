from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cita, Doctor, Paciente, Especialidad
from .forms import CitaForm

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
