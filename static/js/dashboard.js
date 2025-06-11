document.addEventListener('DOMContentLoaded', function() {
    // Inicialización de gráficos si existen
    if(document.getElementById('citasChart')) {
        initializeCitasChart();
    }
    
    // Actualización en tiempo real de citas
    const updateInterval = 60000; // 1 minuto
    setInterval(updateDashboardStats, updateInterval);
});

function initializeCitasChart() {
    // Lógica de gráficos aquí
}

function updateDashboardStats() {
    fetch('/api/dashboard/stats/')
        .then(response => response.json())
        .then(data => {
            updateStatsDisplay(data);
        })
        .catch(error => console.error('Error:', error));
}

function updateStatsDisplay(data) {
    // Actualizar elementos del DOM con nuevos datos
    const elements = {
        'total-citas': data.total_citas,
        'citas-pendientes': data.citas_pendientes,
        'citas-hoy': data.citas_hoy
    };

    Object.entries(elements).forEach(([id, value]) => {
        const element = document.getElementById(id);
        if(element) {
            element.textContent = value;
        }
    });
}
