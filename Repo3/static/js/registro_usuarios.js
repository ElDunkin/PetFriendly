document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const emailInput = document.querySelector('input[name="correo_electronico_usuario"]');
    const idInput = document.querySelector('input[name="numero_documento"]');
    const phoneInput = document.querySelector('input[name="telefono"]');
    const passwordInput = document.querySelector('input[name="contrasena"]');
    const confirmPasswordInput = document.querySelector('input[name="confirmar_contrasena"]');
    const rolSelect = document.querySelector('select[name="id_rol"]');

    form.addEventListener('submit', function (e) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const idRegex = /^\d+$/;
        const phoneRegex = /^\d{10,13}$/;

        let errores = [];

        // Validación de email
        if (!emailRegex.test(emailInput.value)) {
            errores.push("El correo no es válido.");
        }

        // Validación de identificación
        if (!idRegex.test(idInput.value)) {
            errores.push("El número de identificación debe ser numérico.");
        }

        // Validación de teléfono
        if (!phoneRegex.test(phoneInput.value)) {
            errores.push("El número de celular debe tener entre 10 y 13 dígitos.");
        }

        // Validación de contraseñas
        if (passwordInput.value !== confirmPasswordInput.value) {
            errores.push("Las contraseñas no coinciden.");
        }

        // Validación de selección de rol
        if (!rolSelect.value) {
            errores.push("Debe seleccionar un rol válido.");
        }

        // Mostrar errores si existen
        if (errores.length > 0) {
            e.preventDefault();
            alert(errores.join('\n'));
        }
    });
});

btn.addEventListener('click', function () {
    const input = document.getElementById(this.dataset.target);
    const icon = this.querySelector('i');

    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('bi-eye');
        icon.classList.add('bi-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('bi-eye-slash');
        icon.classList.add('bi-eye');
    }
});