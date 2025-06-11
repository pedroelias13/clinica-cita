document.addEventListener('DOMContentLoaded', function() {
    // Manejo de actualización de estado de citas
    const botonesActualizar = document.querySelectorAll('.actualizar-estado');
    botonesActualizar.forEach(boton => {
        boton.addEventListener('click', function() {
            const citaId = this.dataset.citaId;
            actualizarEstadoCita(citaId);
        });
    });
});

function actualizarEstadoCita(citaId) {
    fetch(`/api/citas/${citaId}/actualizar-estado/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        }
    })
    .catch(error => console.error('Error:', error));
}

// Función auxiliar para obtener el token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

class CitaManager {
    constructor() {
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Delegación de eventos para mejor rendimiento
        document.addEventListener('click', (e) => {
            if(e.target.matches('.actualizar-estado')) {
                this.handleActualizarEstado(e);
            }
        });

        const doctorSelect = document.getElementById('id_doctor');
        if(doctorSelect) {
            this.initializeDoctorSelect(doctorSelect);
        }
    }

    handleActualizarEstado(e) {
        const citaId = e.target.dataset.citaId;
        this.actualizarEstadoCita(citaId);
    }

    actualizarEstadoCita(citaId) {
        fetch(`/api/citas/${citaId}/actualizar-estado/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
    }

    // Función auxiliar para obtener el token CSRF
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

// Inicializar cuando el DOM esté listo
const citaManager = new CitaManager();
