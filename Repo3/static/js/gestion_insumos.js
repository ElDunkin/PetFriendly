// Registrar nuevo insumo
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById('nuevoInsumoForm');

    form.onsubmit = async function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        let data = {};
        formData.forEach((v, k) => data[k] = v);

        const res = await fetch('/api/insumos', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify(data)
        });

        if (res.ok) {
            alert('Insumo registrado o actualizado correctamente');
            this.reset();
            cargarInsumos();
        } else {
            const error = await res.json();
            alert('Error: ' + error.error);
        }
    };

    // Cargar insumos al inicio
    cargarInsumos();
});

// Mostrar insumos en tabla
async function cargarInsumos(page = 1) {
    const res = await fetch(`/api/insumos?page=${page}`);
    const data = await res.json();
    const insumos = data.insumos;
    const { page: currentPage, total_pages, per_page } = data;

    let tbody = document.querySelector('#tablaInsumos tbody');
    tbody.innerHTML = '';
    insumos.forEach(ins => {
        tbody.innerHTML += `
            <tr>
                <td>${ins.nombre_insumo}</td>
                <td>${ins.cantidad_inicial}</td>
                <td>${ins.unidad_medida}</td>
                <td>${ins.proveedor}</td>
                <td>${ins.fecha_ingreso}</td>
                <td>${ins.fecha_vencimiento || ''}</td>
                <td>${ins.tipo_insumo}</td>
            </tr>`;
    });

    // Generate pagination controls
    const paginationControls = document.getElementById('paginationControls');
    paginationControls.innerHTML = '';

    // Previous button
    if (currentPage > 1) {
        paginationControls.innerHTML += `<li class="page-item"><a class="page-link" href="#" onclick="cargarInsumos(${currentPage - 1})">Anterior</a></li>`;
    } else {
        paginationControls.innerHTML += `<li class="page-item disabled"><span class="page-link">Anterior</span></li>`;
    }

    // Page numbers
    for (let i = 1; i <= total_pages; i++) {
        if (i === currentPage) {
            paginationControls.innerHTML += `<li class="page-item active"><span class="page-link">${i}</span></li>`;
        } else {
            paginationControls.innerHTML += `<li class="page-item"><a class="page-link" href="#" onclick="cargarInsumos(${i})">${i}</a></li>`;
        }
    }

    // Next button
    if (currentPage < total_pages) {
        paginationControls.innerHTML += `<li class="page-item"><a class="page-link" href="#" onclick="cargarInsumos(${currentPage + 1})">Siguiente</a></li>`;
    } else {
        paginationControls.innerHTML += `<li class="page-item disabled"><span class="page-link">Siguiente</span></li>`;
    }
}
cargarInsumos();

// Mostrar alerta de stock mínimo o vencimiento
async function mostrarAlerta() {    
    const res = await fetch('/api/alertas');
    const alertas = await res.json();
    let lista = document.getElementById('alertaLista');
    lista.innerHTML = '';
    if (alertas.length === 0) {
        lista.innerHTML = '<li>No hay alertas.</li>';
    } else {
        alertas.forEach(a => {
            lista.innerHTML += `<li>${a.nombre_insumo} - Stock: ${a.cantidad_inicial} - Vence: ${a.fecha_vencimiento || 'N/A'}</li>`;
        });
    }
    document.getElementById('alertaModal').style.display = 'flex';
}
function cerrarAlerta() {
    document.getElementById('alertaModal').style.display = 'none';
}

document.addEventListener("DOMContentLoaded", () => {
    // Evitar fechas anteriores a hoy
    const hoy = new Date().toISOString().split("T")[0];
    document.getElementById("fecha_vencimiento").setAttribute("min", hoy);

    // ... tu código del form y cargarInsumos()
});