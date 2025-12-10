document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.btn-editar').forEach(button => {
        button.addEventListener('click', () => {
            const usuario = {
                numero_documento: button.getAttribute('data-numero'),
                nombre_usuario: button.getAttribute('data-nombre'),
                apellido_usuario: button.getAttribute('data-apellido'),
                correo_electronico_usuario: button.getAttribute('data-correo'),
                telefono: button.getAttribute('data-telefono')
            };

            document.getElementById('numero_documento_editar').value = usuario.numero_documento;
            document.getElementById('nombre_usuario').value = usuario.nombre_usuario;
            document.getElementById('apellido_usuario').value = usuario.apellido_usuario;
            document.getElementById('correo_electronico_usuario').value = usuario.correo_electronico_usuario;
            document.getElementById('telefono').value = usuario.telefono;

            document.getElementById('formEditar').action = `/modificar_usuarios/${usuario.numero_documento}`;

            const modal = new bootstrap.Modal(document.getElementById('modalEditar'));
            modal.show();
        });
    });
});
