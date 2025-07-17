// Registrar nuevo insumo
document.getElementById('nuevoInsumoForm').onsubmit = async function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    let data = {};
    formData.forEach((v, k) => data[k] = v);

    await fetch('/api/insumos', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(data)
    });
    alert('¡Insumo registrado!');
    this.reset();
    cargarInsumos();
};

// Mostrar insumos en tabla
async function cargarInsumos() {
    const res = await fetch('/api/insumos');
    const insumos = await res.json();
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