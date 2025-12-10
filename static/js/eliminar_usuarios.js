function abrirModalEliminar(nombre) {
    usuarioAEliminar = nombre; // Aquí puedes usar el ID real en una app completa
    document.getElementById('mensajeEliminar').innerText = `¿Estás seguro de eliminar a ${nombre}?`;
    document.getElementById('modalEliminar').style.display = 'flex';
}

function cerrarModalEliminar() {
    document.getElementById('modalEliminar').style.display = 'none';
}

function confirmarEliminacion() {
    alert(`Usuario "${usuarioAEliminar}" eliminado (simulación)`);
    cerrarModalEliminar();
}

function confirmarEliminacion(nombre, url) {
    document.getElementById('nombreUsuarioEliminar').textContent = nombre;
    document.getElementById('btnConfirmarEliminar').href = url;
    let modal = new bootstrap.Modal(document.getElementById('modalEliminar'));
    modal.show();
}