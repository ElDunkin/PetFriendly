document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const fechaInput = document.getElementById('fecha_consulta');
    const horaInput = document.getElementById('hora_consulta');

    form.addEventListener('submit', function (e) {
        const fecha = fechaInput.value;
        const hora = horaInput.value;

        if (!fecha || !hora) return; // deja que HTML5 valide lo demás

        const fechaSeleccionada = new Date(`${fecha}T${hora}`);
        const ahora = new Date();

        if (fechaSeleccionada < ahora) {
            e.preventDefault();
            alert("No puedes registrar una consulta en el pasado.");
        }
    });
});
