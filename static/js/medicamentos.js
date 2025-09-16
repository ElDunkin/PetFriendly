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
            alert('Medicamento registrado o actualizado');
        }
    };

    // Registrar Movimiento (Entrada/Salida)
    document.getElementById('formMovimiento').onsubmit = async function(e) {
        e.preventDefault();
        const form = this;
        const data = Object.fromEntries(new FormData(form).entries());
        data['cantidad'] = parseInt(data['cantidad']);
        data['id_medicamento'] = parseInt(data['medicamento_id']);

        // Validaciones frontend
        if (data['cantidad'] <= 0) {
            alert("La cantidad debe ser mayor a cero");
            return;
        }

        // Comprobar existencia para Salida
        if (data['tipo'] === 'Salida') {
            const fila = Array.from(document.querySelectorAll('#tablaMedicamentos tbody tr'))
                .find(tr => parseInt(tr.querySelector('button.btn-success, button.btn-danger').getAttribute('onclick').match(/\d+/)[0]) === data['id_medicamento']);
            const existencia_actual = parseInt(fila.children[1].innerText);
            if (data['cantidad'] > existencia_actual) {
                alert("No hay suficiente stock para esta salida");
                return;
            }
        }

        // Validar responsable como número
        if (!/^\d+$/.test(data['responsable'])) {
            alert("El campo Responsable debe ser un número de documento válido");
            return;
        }

        const res = await fetch('/api/movimientos', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        const result = await res.json();

        if (!res.ok) {
            alert(result.error);
        } else {
            cerrarModal('modalMovimiento');
            cargarMedicamentos();
            alert('Movimiento registrado');
        }
    };

    // Buscar medicamentos
    document.getElementById('search').addEventListener('input', function() {
        let term = this.value.toLowerCase();
        document.querySelectorAll('#tablaMedicamentos tbody tr').forEach(tr => {
            let text = tr.innerText.toLowerCase();
            tr.style.display = text.includes(term) ? '' : 'none';
        });
    });
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
                <button class="btn btn-sm btn-success" onclick="abrirMovimiento(${m.id_medicamento}, 'Entrada')">Entrada</button>
                <button class="btn btn-sm btn-danger" onclick="abrirMovimiento(${m.id_medicamento}, 'Salida')">Salida</button>
                <button class="btn btn-sm btn-info" onclick="verHistorial(${m.id_medicamento})">Historial</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

window.abrirMovimiento = function(id_medicamento, tipo) {
    document.getElementById('mov_medicamento_id').value = id_medicamento;
    document.getElementById('mov_tipo').value = tipo;
    document.getElementById('formMovimiento').reset();

    // Mostrar mensaje si Salida y stock 0
    if (tipo === 'Salida') {
        const fila = Array.from(document.querySelectorAll('#tablaMedicamentos tbody tr'))
            .find(tr => parseInt(tr.querySelector('button.btn-danger').getAttribute('onclick').match(/\d+/)[0]) === id_medicamento);
        const existencia_actual = parseInt(fila.children[1].innerText);
        if (existencia_actual === 0) {
            alert("No hay stock disponible para salida");
            return;
        }
    }

    mostrarModal('modalMovimiento');
};

window.verHistorial = async function(id_medicamento) {
    const res = await fetch(`/api/movimientos/${id_medicamento}`);
    const movs = await res.json();
    let tbody = document.querySelector('#tablaMovimientos tbody');
    tbody.innerHTML = '';

    if (movs.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="text-center">No hay movimientos registrados para este medicamento</td></tr>`;
    } else {
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
    }

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