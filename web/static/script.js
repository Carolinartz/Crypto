let datosAnteriores = {};
let chart = null;
let historialChart = null;

// Carga datos generales y dibuja tabla + gráfico de barras
async function cargarDatos() {
    const res = await fetch('/api/criptos');
    const datos = await res.json();

    const tbody = document.getElementById('tabla-body');
    tbody.innerHTML = '';

    datos.forEach(row => {
        const tr = document.createElement('tr');
        const anterior = datosAnteriores[row.simbolo];

        if (anterior) {
            if (row.precio_usd > anterior.precio_usd) {
                tr.classList.add('subio');
            } else if (row.precio_usd < anterior.precio_usd) {
                tr.classList.add('bajo');
            }

            setTimeout(() => {
                tr.classList.remove('subio');
                tr.classList.remove('bajo');
            }, 1000);
        }

        tr.innerHTML = `
            <td>${row.simbolo}</td>
            <td>${row.precio_usd?.toFixed(2)}</td>
            <td>${row.max_1h !== null ? row.max_1h.toFixed(2) : '-'}</td>
            <td>${row.min_1h !== null ? row.min_1h.toFixed(2) : '-'}</td>
            <td>${row.prom_1h !== null ? row.prom_1h.toFixed(2) : '-'}</td>
            <td><strong>${row.senal}</strong></td>
        `;

        // Hacer clic en la fila para mostrar historial
        tr.addEventListener('click', () => {
            mostrarHistorial(row.simbolo);
        });

        tbody.appendChild(tr);
        datosAnteriores[row.simbolo] = row;
    });

    actualizarGrafica(datos);
}

// Gráfico de barras comparativo
function actualizarGrafica(datos) {
    const labels = datos.map(d => d.simbolo);
    const precios = datos.map(d => d.precio_usd);

    const ctx = document.getElementById('chart-precios').getContext('2d');

    if (chart) {
        chart.data.labels = labels;
        chart.data.datasets[0].data = precios;
        chart.update();
    } else {
        chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Precio Actual (USD)',
                    data: precios,
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: false }
                }
            }
        });
    }
}

// Mostrar historial por símbolo al hacer clic
function mostrarHistorial(simbolo) {
    fetch(`/api/historial/${simbolo}`)
        .then(res => res.json())
        .then(data => {
            const labels = data.map(p => new Date(p.fecha).toLocaleTimeString());
            const precios = data.map(p => p.precio);

            const ctx = document.getElementById('chart-historial').getContext('2d');
            document.getElementById('titulo-historial').textContent = `Historial de ${simbolo}`;
            document.getElementById('titulo-historial').style.display = 'block';

            if (historialChart) {
                historialChart.data.labels = labels;
                historialChart.data.datasets[0].data = precios;
                historialChart.data.datasets[0].label = `Precio de ${simbolo}`;
                historialChart.update();
            } else {
                historialChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: `Precio de ${simbolo}`,
                            data: precios,
                            fill: false,
                            borderColor: 'rgba(255, 99, 132, 1)',
                            tension: 0.1
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: { beginAtZero: false }
                        }
                    }
                });
            }
        });
}

// Inicialización
cargarDatos();
setInterval(cargarDatos, 100);
