document.addEventListener('DOMContentLoaded', function () {
    cargarMedicamentos();

    // Registrar Medicamento
    document.getElementById('formMedicamento').onsubmit = async function (e) {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(this).entries());
        data['cantidad_inicial'] = parseInt(data['cantidad_inicial']);

        const res = await fetch('/api/medicamentos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (res.ok) {
            this.reset();
            cargarMedicamentos();
            alert('Medicamento registrado o actualizado');
        }
    };

    // Registrar Movimiento
    document.getElementById('formMovimiento').onsubmit = async function (e) {
        e.preventDefault();
        const form = this;
        const data = Object.fromEntries(new FormData(form).entries());

        data['cantidad'] = parseInt(data['cantidad']);
        data['id_medicamento'] = parseInt(data['medicamento_id']);

        if (data['cantidad'] <= 0) {
            alert("La cantidad debe ser mayor a cero");
            return;
        }

        // Validación de Salida
        if (data['tipo'] === 'Salida') {
            const fila = [...document.querySelectorAll('#tablaMedicamentos tbody tr')]
                .find(tr => tr.innerHTML.includes(`abrirMovimiento(${data['id_medicamento']}, 'Salida')`));

            if (!fila) {
                alert("No se encontró el medicamento en la tabla.");
                return;
            }

            const existencia_actual = parseInt(fila.children[1].innerText);

            if (data['cantidad'] > existencia_actual) {
                alert("No hay suficiente stock para esta salida");
                return;
            }
        }

        // Validar documento
        if (!/^\d+$/.test(data['responsable'])) {
            alert("El campo Responsable debe ser un número válido");
            return;
        }

        const res = await fetch('/api/movimientos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        let result;
        try {
            result = await res.json();
        } catch {
            alert("Error interno del servidor.");
            return;
        }

        if (!res.ok) {
            alert(result.error || "Error registrando movimiento");
        } else {
            cerrarModal('modalMovimiento');
            cargarMedicamentos();
            alert('Movimiento registrado');
        }
    };

    // Buscador
    document.getElementById('search').addEventListener('input', function () {
        let term = this.value.toLowerCase();
        document.querySelectorAll('#tablaMedicamentos tbody tr').forEach(tr => {
            tr.style.display = tr.innerText.toLowerCase().includes(term) ? '' : 'none';
        });
    });
});

// Cargar medicamentos
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
            <td>${m.lote}</td> 
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

window.abrirMovimiento = function (id_medicamento, tipo) {
    document.getElementById('mov_medicamento_id').value = id_medicamento;
    document.getElementById('mov_tipo').value = tipo;
    document.getElementById('formMovimiento').reset();

    // Cargar veterinarios
    const select = document.querySelector('select[name="responsable"]');
    fetch('/api/veterinarios')
    .then(res => res.json())
    .then(vets => {
        select.innerHTML = '<option value="">Seleccionar responsable *</option>';
        vets.forEach(v => {
            select.innerHTML += `<option value="${v.numero_documento}">${v.numero_documento} - ${v.nombre} ${v.apellido}</option>`;
        });
    })
    .catch(err => {
        console.error('Error cargando veterinarios:', err);
        alert('Error cargando lista de responsables');
    });

    // Si es salida validar stock
    if (tipo === 'Salida') {
        const fila = [...document.querySelectorAll('#tablaMedicamentos tbody tr')]
            .find(tr => tr.innerHTML.includes(`abrirMovimiento(${id_medicamento}, 'Salida')`));

        if (fila) {
            const stock = parseInt(fila.children[1].innerText);
            if (stock === 0) {
                alert("No hay stock disponible para salida");
                return;
            }
        }
    }

    mostrarModal('modalMovimiento');
};

window.verHistorial = async function (id_medicamento) {
    const modalBody = document.querySelector('#tablaMovimientos tbody');

    if (!modalBody) {
        alert("ERROR: No existe el modal 'modalHistorial' con la tabla de movimientos.");
        return;
    }

    let res = await fetch(`/api/movimientos/${id_medicamento}`);
    let movs;

    try {
        movs = await res.json();
    } catch {
        alert("⚠ Error obteniendo historial. La API devolvió HTML en lugar de JSON (probable error 500).");
        return;
    }

    modalBody.innerHTML = '';

    if (!Array.isArray(movs) || movs.length === 0) {
        modalBody.innerHTML = `<tr><td colspan="6" class="text-center">No hay movimientos registrados</td></tr>`;
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
            modalBody.appendChild(tr);
        });
    }

    mostrarModal('modalHistorial');
};

// Modales manuales
function mostrarModal(id) {
    const modal = document.getElementById(id);
    modal.classList.add('show');
    modal.style.display = 'flex';
}

function cerrarModal(id) {
    const modal = document.getElementById(id);
    modal.classList.remove('show');
    modal.style.display = 'none';
}

document.querySelectorAll('.btn-close, .btn-secondary').forEach(btn => {
    btn.addEventListener('click', function () {
        cerrarModal(btn.closest('.modal').id);
    });
});
