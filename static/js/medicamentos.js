document.addEventListener('DOMContentLoaded', function () {
    cargarMedicamentos();

    // 🟢 1. Registrar/Editar Medicamento
    document.getElementById('formMedicamento').onsubmit = async function(e) {
        e.preventDefault();
        const form = this;
        const data = Object.fromEntries(new FormData(form).entries());
        
        const id_medicamento_edit = form.querySelector('#id_medicamento_edit').value;
        
        let method = 'POST';
        let url = '/api/medicamentos';
        let successMessage = 'Medicamento registrado';

        if (id_medicamento_edit) {
            // Modo Edición (PUT)
            method = 'PUT';
            url = `/api/medicamentos/${id_medicamento_edit}`;
            successMessage = 'Medicamento actualizado';
            // Eliminamos la cantidad_inicial en modo edición
            delete data['cantidad_inicial']; 
        } else {
            // Modo Registro (POST)
            data['cantidad_inicial'] = parseInt(data['cantidad_inicial']);
        }
        
        const res = await fetch(url, {
            method: method,
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        
        if (res.ok) {
            form.reset();
            cargarMedicamentos();
            
            // Restablecer el formulario a modo "Registro"
            form.querySelector('#id_medicamento_edit').value = '';
            document.getElementById('btn-submit-medicamento').innerText = 'Registrar';
            document.getElementById('cantidad_inicial_input').required = true;
            document.getElementById('cantidad_inicial_input').style.display = 'block';

            alert(successMessage);
        } else {
            const error = await res.json();
            alert(`Error: ${error.error || 'Ha ocurrido un error en el servidor.'}`);
        }
    };

    // 2. Registrar Movimiento (Entrada/Salida) - (Lógica sin cambios)
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
                .find(tr => {
                    const buttons = tr.querySelectorAll('button.btn-success, button.btn-danger');
                    if (buttons.length > 0) {
                        return parseInt(buttons[0].getAttribute('onclick').match(/\d+/)[0]) === data['id_medicamento'];
                    }
                    return false;
                });
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

    // 3. Buscar medicamentos - (Lógica sin cambios)
    document.getElementById('search').addEventListener('input', function() {
        let term = this.value.toLowerCase();
        document.querySelectorAll('#tablaMedicamentos tbody tr').forEach(tr => {
            let text = tr.innerText.toLowerCase();
            tr.style.display = text.includes(term) ? '' : 'none';
        });
    });
});

// ... dentro de medicamentos.js
async function cargarMedicamentos() {
    const res = await fetch('/api/medicamentos');
    const meds = await res.json();
    let tbody = document.querySelector('#tablaMedicamentos tbody');
    tbody.innerHTML = '';
    meds.forEach(m => {
        let tr = document.createElement('tr');
        // Reemplaza btn-sm con btn-super-sm en TODOS los botones
    tr.innerHTML = `
        <td>${m.nombre_medicamento}</td>
        <td>${m.existencia}</td>
        <td>${m.estado}</td>
        <td>${m.fecha_vencimiento}</td>
        <td>
            <button class="btn btn-super-sm btn-success" onclick="abrirMovimiento(${m.id_medicamento}, 'Entrada')">Entrada</button>
            <button class="btn btn-super-sm btn-danger" onclick="abrirMovimiento(${m.id_medicamento}, 'Salida')">Salida</button>
            <button class="btn btn-super-sm btn-info" onclick="verHistorial(${m.id_medicamento})">Historial</button>
            <button class="btn btn-super-sm btn-warning" onclick="editarMedicamento(${m.id_medicamento})">Editar</button>
            <button class="btn btn-super-sm btn-dark" onclick="eliminarMedicamento(${m.id_medicamento})">Eliminar</button>
        </td>
    `;
    tbody.appendChild(tr);
    });
}

// 🟢 5. Función para cargar datos para la edición
window.editarMedicamento = async function(id_medicamento) {
    const res = await fetch(`/api/medicamentos/${id_medicamento}`);
    if (!res.ok) {
        alert('Error al cargar datos del medicamento.');
        return;
    }
    const m = await res.json();
    
    // Ocultar el campo de cantidad inicial y quitar el 'required'
    document.getElementById('cantidad_inicial_input').required = false; 
    document.getElementById('cantidad_inicial_input').style.display = 'none';

    // Rellenar el formulario
    document.getElementById('id_medicamento_edit').value = m.id_medicamento;
    document.querySelector('[name="nombre_medicamento"]').value = m.nombre_medicamento;
    document.querySelector('[name="principio_activo"]').value = m.principio_activo;
    document.querySelector('[name="presentacion"]').value = m.presentacion;
    document.querySelector('[name="lote"]').value = m.lote;
    document.querySelector('[name="concentracion"]').value = m.concentracion;
    document.querySelector('[name="fecha_vencimiento"]').value = m.fecha_vencimiento;
    document.querySelector('[name="proveedor"]').value = m.proveedor;
    document.querySelector('[name="observaciones"]').value = m.observaciones;
    
    // Actualizar el texto del botón
    document.getElementById('btn-submit-medicamento').innerText = 'Guardar Cambios';

    alert('Datos cargados para edición. Modifica y haz clic en "Guardar Cambios".');
};

// 🟢 6. Función para eliminar un medicamento
window.eliminarMedicamento = async function(id_medicamento) {
    if (!confirm(`¿Estás seguro de que deseas eliminar el medicamento con ID ${id_medicamento} y todos sus movimientos asociados? Esta acción es irreversible.`)) {
        return;
    }

    const res = await fetch(`/api/medicamentos/${id_medicamento}`, {
        method: 'DELETE'
    });

    if (res.ok) {
        cargarMedicamentos();
        alert('Medicamento eliminado correctamente');
    } else {
        const error = await res.json();
        alert(`Error al eliminar: ${error.error || 'Desconocido'}`);
    }
};

window.abrirMovimiento = function(id_medicamento, tipo) {
    document.getElementById('mov_medicamento_id').value = id_medicamento;
    document.getElementById('mov_tipo').value = tipo;
    document.getElementById('formMovimiento').reset();

    // Mostrar mensaje si Salida y stock 0
    if (tipo === 'Salida') {
        const fila = Array.from(document.querySelectorAll('#tablaMedicamentos tbody tr'))
            .find(tr => {
                const buttons = tr.querySelectorAll('button.btn-success, button.btn-danger');
                if (buttons.length > 0) {
                    return parseInt(buttons[0].getAttribute('onclick').match(/\d+/)[0]) === id_medicamento;
                }
                return false;
            });

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