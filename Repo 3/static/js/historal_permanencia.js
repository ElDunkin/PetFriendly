function abrirHistorialPermanencia(id) {
    const modalEl = document.getElementById("modal_Historial_" + id);
    if (!modalEl) {
        console.error("No se encontró el modal para el animal:", id);
        return;
    }
    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
    modal.show();
}