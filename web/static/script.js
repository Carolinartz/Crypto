let datosAnteriores = {};
let chart = null;
let historialChart = null;

// Diccionario de nombres por símbolo
const nombreMap = {
    BTC: "Bitcoin",
    ETH: "Ethereum",
    USDT: "Tether",
    BNB: "BNB",
    SOL: "Solana",
    XRP: "Ripple",
    DOGE: "Dogecoin",
    ADA: "Cardano",
    DOT: "Polkadot",
    MATIC: "Polygon",
    SHIB: "Shiba Inu",
    AVAX: "Avalanche",
    LTC: "Litecoin",
    TRX: "TRON"
};

async function cargarDatos() {
    const res = await fetch('/api/criptos');
    const datos = await res.json();

    const tbody = document.getElementById('tabla-body');
    tbody.innerHTML = '';

    datos.forEach(row => {
        const tr = document.createElement('tr');
        const anterior = datosAnteriores[row.simbolo];
        const nombre = nombreMap[row.simbolo] || row.simbolo;

        // Pintar según señal: rojo si es 'B' (buy), verde en caso contrario
        if (row.senal === 'B') {
            tr.classList.add('vender'); // rojo claro
        } else {
            tr.classList.add('comprar'); // verde claro
        }

        // Efecto temporal si cambia el precio
        if (anterior) {
            if (row.precio_usd > anterior.precio_usd) tr.classList.add('subio');
            if (row.precio_usd < anterior.precio_usd) tr.classList.add('bajo');
            setTimeout(() => {
                tr.classList.remove('subio', 'bajo');
            }, 1000);
        }

        tr.innerHTML = `
            <td>${row.simbolo}</td>
            <td>${nombre}</td>
            <td>${row.precio_usd?.toFixed(2)}</td>
            <td>${row.max_1h !== null ? row.max_1h.toFixed(2) : '-'}</td>
            <td>${row.min_1h !== null ? row.min_1h.toFixed(2) : '-'}</td>
            <td>${row.prom_1h !== null ? row.prom_1h.toFixed(2) : '-'}</td>
            <td><strong>${row.senal}</strong></td>
            <td>${new Date(row.fecha).toLocaleString()}</td>
        `;

        tr.addEventListener('click', () => {
            mostrarHistorial(row.simbolo);
        });

        tbody.appendChild(tr);
        datosAnteriores[row.simbolo] = row;
    });

    actualizarGrafica(datos);
}

function actualizarGrafica(datos) {
    const unicos = {};
    datos.forEach(d => {
        if (!unicos[d.simbolo]) unicos[d.simbolo] = d;
    });

    const labels = Object.keys(unicos);
    const precios = labels.map(s => unicos[s].precio_usd);
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

cargarDatos();
setInterval(cargarDatos, 1000);
