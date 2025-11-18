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

                    });
    });
});
