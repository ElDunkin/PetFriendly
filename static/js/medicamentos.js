document.addEventListener('DOMContentLoaded', function () {
    cargarMedicamentos();

    // Registrar Medicamento
    document.getElementById('formMedicamento').onsubmit = async function(e) {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(this).entries());
        data['cantidad_inicial'] = parseInt(data['cantidad_inicial']);
        const res = await fetch('/api/medicamentos', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if (res.ok) {
            this.reset();
            cargarMedicamentos();
            alert('Medicamento registrado');
        }
    };

    // Registrar Movimiento (Entrada/Salida)
    document.getElementById('formMovimiento').onsubmit = async function(e) {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(this).entries());
        data['cantidad'] = parseInt(data['cantidad']);
        data['medicamento_id'] = parseInt(data['medicamento_id']);
        const res = await fetch('/api/movimientos', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if (res.ok) {
            cerrarModal('modalMovimiento');
            cargarMedicamentos();
            alert('Movimiento registrado');
        }
    };
});

async function cargarMedicamentos() {
    const res = await fetch('/api/medicamentos');
    const meds = await res.json();
    let tbody = document.querySelector('#tablaMedicamentos tbody');
    tbody.innerHTML = '';
    meds.forEach(m => {
        let tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${m.nombre_medicamento}</td>
            <td>${m.existencia}</td>
            <td>${m.estado}</td>
            <td>${m.fecha_vencimiento}</td>
            <td>
                <button class="btn btn-sm btn-success" onclick="abrirMovimiento(${m.id}, 'Entrada')">Entrada</button>
                <button class="btn btn-sm btn-danger" onclick="abrirMovimiento(${m.id}, 'Salida')">Salida</button>
                <button class="btn btn-sm btn-info" onclick="verHistorial(${m.id})">Historial</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

window.abrirMovimiento = function(id, tipo) {
    document.getElementById('mov_medicamento_id').value = id;
    document.getElementById('mov_tipo').value = tipo;
    mostrarModal('modalMovimiento');
};

window.verHistorial = async function(id) {
    const res = await fetch(`/api/movimientos/${id}`);
    const movs = await res.json();
    let tbody = document.querySelector('#tablaMovimientos tbody');
    tbody.innerHTML = '';
    movs.forEach(m => {
        let tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${m.fecha}</td>
            <td>${m.accion}</td>
            <td>${m.responsable}</td>
            <td>${m.motivo}</td>
            <td>${m.cantidad}</td>
            <td>${m.observacion || ''}</td>
        `;
        tbody.appendChild(tr);
    });
    mostrarModal('modalHistorial');
};

// Mostrar y cerrar modales manuales
function mostrarModal(id) {
    document.getElementById(id).classList.add('show');
    document.getElementById(id).style.display = 'flex';
}
function cerrarModal(id) {
    document.getElementById(id).classList.remove('show');
    document.getElementById(id).style.display = 'none';
}

// Cierre de modales con btn-close
document.querySelectorAll('.btn-close, .btn-secondary').forEach(btn => {
    btn.addEventListener('click', function() {
        let modal = btn.closest('.modal');
        cerrarModal(modal.id);
    });
});