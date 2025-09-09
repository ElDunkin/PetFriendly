document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", function (e) {
        const nombre = form.nombre.value.trim();
        if (nombre.length < 3) {
            e.preventDefault();
            alert("Por favor ingresa un nombre de jornada válido.xd");
        }
    });
});
