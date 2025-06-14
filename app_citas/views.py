from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Cita, Doctor, Paciente, Especialidad, Genero, TipoSangre
from django.utils import timezone
from django.contrib.auth.models import User
from .forms import CitaForm, RegistroForm
from datetime import date, timedelta
import json

@login_required
def lista_citas(request):
    if hasattr(request.user, 'doctor'):
        citas = Cita.objects.filter(doctor__usuario=request.user)
    elif hasattr(request.user, 'paciente'):
        citas = Cita.objects.filter(paciente__usuario=request.user)
    else:
        citas = []
    
    context = {
        'citas': citas,
        'titulo': 'Mis Citas'
    }
    return render(request, 'app_citas/lista_citas.html', context)

@login_required
def crear_cita(request):
    if not hasattr(request.user, 'paciente'):
        messages.error(request, "Solo los pacientes pueden agendar citas.")
        return redirect('app_citas:dashboard')

    from datetime import date, timedelta, datetime

    doctores = Doctor.objects.filter(activo=True)
    fecha_hoy = date.today()
    dias_mostrar = 7

    disponibilidad = []
    for doctor in doctores:
        dias = []
        for i in range(dias_mostrar):
            fecha = fecha_hoy + timedelta(days=i)
            horarios = []
            hora_actual = doctor.horario_inicio
            while hora_actual < doctor.horario_fin:
                if not Cita.objects.filter(doctor=doctor, fecha=fecha, hora=hora_actual, estado__in=['PENDIENTE', 'CONFIRMADA']).exists():
                    horarios.append(hora_actual.strftime('%H:%M'))
                dt = datetime.combine(fecha, hora_actual) + timedelta(hours=1)
                hora_actual = dt.time()
            if horarios:
                dias.append({'fecha': fecha.strftime('%Y-%m-%d'), 'horas': horarios})
        if dias:
            disponibilidad.append({'doctor': doctor, 'dias': dias})

    # Mensaje de ayuda si no hay doctores o no hay horarios
    if not disponibilidad:
        messages.info(request, "No hay doctores disponibles o no hay horarios libres en los próximos días.")

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        motivo = request.POST.get('motivo')
        tipo_cita = request.POST.get('tipo_cita')
        if doctor_id and fecha and hora and motivo and tipo_cita:
            doctor = get_object_or_404(Doctor, pk=doctor_id)
            fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()
            hora_dt = datetime.strptime(hora, "%H:%M").time()
            if hora_dt < doctor.horario_inicio or hora_dt >= doctor.horario_fin:
                messages.error(request, "La hora seleccionada está fuera del horario laboral del doctor.")
            elif Cita.objects.filter(doctor=doctor, fecha=fecha_dt, hora=hora_dt, estado__in=['PENDIENTE', 'CONFIRMADA']).exists():
                messages.error(request, "El horario seleccionado ya está ocupado.")
            else:
                Cita.objects.create(
                    paciente=request.user.paciente,
                    doctor=doctor,
                    fecha=fecha_dt,
                    hora=hora_dt,
                    motivo=motivo,
                    tipo_cita=tipo_cita,
                    estado='PENDIENTE'
                )
                messages.success(request, "Cita agendada correctamente.")
                return redirect('app_citas:lista_citas')
        else:
            messages.error(request, "Debes completar todos los campos y seleccionar un horario disponible.")
    return render(request, 'app_citas/citas/crear_cita.html', {
        'disponibilidad': disponibilidad,
        'disponibilidad_json': json.dumps([
            {
                'doctor': {
                    'id': d['doctor'].id,
                    'usuario': {'get_full_name': d['doctor'].usuario.get_full_name()},
                    'especialidad_principal': str(d['doctor'].especialidad_principal)
                },
                'dias': d['dias']
            } for d in disponibilidad
        ]),
        'titulo': 'Agendar Nueva Cita'
    })

@login_required
def lista_especialidades(request):
    especialidades = Especialidad.objects.all()
    return render(request, 'app_citas/lista_especialidades.html', {
        'especialidades': especialidades
    })

@login_required
def lista_doctores(request):
    doctores = Doctor.objects.select_related('usuario', 'especialidad_principal').filter(activo=True)
    return render(request, 'app_citas/doctores/lista_doctores.html', {
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
        return redirect_user_by_role(request.user)
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect_user_by_role(user)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            
    return render(request, 'registration/login.html')

def redirect_user_by_role(user):
    if user.is_superuser:
        return redirect('app_citas:admin_dashboard')
    elif hasattr(user, 'doctor'):
        return redirect('app_citas:doctor_dashboard')
    elif hasattr(user, 'paciente'):
        return redirect('app_citas:paciente_dashboard')
    return redirect('app_citas:dashboard')

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
            return redirect('app_citas:dashboard')  # Cambiar aquí
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('app_citas:dashboard')
        
    context = {
        'total_citas': Cita.objects.count(),
        'total_doctores': Doctor.objects.count(),
        'total_pacientes': Paciente.objects.count(),
        'citas_hoy': Cita.objects.filter(fecha=timezone.now().date()),
        'doctores_activos': Doctor.objects.filter(activo=True).count(),
        'citas_pendientes': Cita.objects.filter(estado='PENDIENTE').count()
    }
    return render(request, 'app_citas/admin_dashboard.html', context)

@login_required
def doctor_dashboard(request):
    context = {
        'citas_hoy': Cita.objects.filter(
            doctor__usuario=request.user,
            fecha=timezone.now().date()
        )
    }
    return render(request, 'app_citas/doctor_dashboard.html', context)

@login_required
def paciente_dashboard(request):
    context = {
        'mis_citas': Cita.objects.filter(paciente__usuario=request.user),
        'proxima_cita': Cita.objects.filter(
            paciente__usuario=request.user,
            fecha__gte=timezone.now().date()
        ).first()
    }
    return render(request, 'app_citas/paciente_dashboard.html', context)

@login_required
def editar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if not (request.user.is_superuser or (hasattr(request.user, 'paciente') and cita.paciente.usuario == request.user)):
        messages.error(request, "No tienes permiso para editar esta cita.")
        return redirect('app_citas:lista_citas')
    if not cita.is_modificable():
        messages.error(request, "No se puede modificar esta cita.")
        return redirect('app_citas:lista_citas')
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            nueva_cita = form.save(commit=False)
            # Validación de horario
            if nueva_cita.hora < nueva_cita.doctor.horario_inicio or nueva_cita.hora >= nueva_cita.doctor.horario_fin:
                messages.error(request, "La hora seleccionada está fuera del horario del doctor.")
                return render(request, 'app_citas/citas/editar_cita.html', {'form': form, 'cita': cita})
            # Validación de duplicidad
            if Cita.objects.filter(doctor=nueva_cita.doctor, fecha=nueva_cita.fecha, hora=nueva_cita.hora, estado__in=['PENDIENTE', 'CONFIRMADA']).exclude(pk=cita.pk).exists():
                messages.error(request, "Ya existe una cita para ese horario con este doctor.")
                return render(request, 'app_citas/citas/editar_cita.html', {'form': form, 'cita': cita})
            nueva_cita.save()
            messages.success(request, "Cita reagendada correctamente.")
            return redirect('app_citas:lista_citas')
    else:
        form = CitaForm(instance=cita)
    return render(request, 'app_citas/citas/editar_cita.html', {'form': form, 'cita': cita})

@login_required
def cancelar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.user.is_superuser or \
       (hasattr(request.user, 'paciente') and cita.paciente.usuario == request.user):
        if cita.is_modificable():
            cita.estado = 'CANCELADA'
            cita.save()
            messages.success(request, "La cita fue cancelada correctamente.")
        else:
            messages.error(request, "No se puede cancelar esta cita.")
    else:
        messages.error(request, "No tienes permiso para cancelar esta cita.")
    return redirect('app_citas:lista_citas')

@login_required
def historial_citas(request):
    if hasattr(request.user, 'doctor'):
        citas = Cita.objects.filter(doctor__usuario=request.user).exclude(estado='PENDIENTE')
    elif hasattr(request.user, 'paciente'):
        citas = Cita.objects.filter(paciente__usuario=request.user).exclude(estado='PENDIENTE')
    else:
        citas = []
    context = {
        'citas': citas,
        'titulo': 'Historial de Citas'
    }
    return render(request, 'app_citas/historial_citas.html', context)

@login_required
def perfil(request):
    user = request.user
    perfil = None
    if hasattr(user, 'paciente'):
        perfil = user.paciente
    elif hasattr(user, 'doctor'):
        perfil = user.doctor
    return render(request, 'app_citas/perfil.html', {'user': user, 'perfil': perfil})

@login_required
def editar_perfil(request):
    user = request.user
    if hasattr(user, 'paciente'):
        perfil = user.paciente
        from .forms import RegistroForm
        if request.method == 'POST':
            form = RegistroForm(request.POST, instance=user)
            if form.is_valid():
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.save()
                perfil.telefono = form.cleaned_data['telefono']
                perfil.direccion = form.cleaned_data['direccion']
                perfil.save()
                messages.success(request, "Perfil actualizado correctamente.")
                return redirect('app_citas:perfil')
        else:
            initial = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'telefono': perfil.telefono,
                'direccion': perfil.direccion,
            }
            form = RegistroForm(initial=initial)
        return render(request, 'app_citas/editar_perfil.html', {'form': form})
    messages.error(request, "Solo pacientes pueden editar su perfil en esta versión.")
    return redirect('app_citas:perfil')

# Recomendación: realiza backups periódicos de la base de datos (db.sqlite3) y cuida la privacidad de los datos de tus usuarios.
