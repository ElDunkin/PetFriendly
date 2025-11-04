document.addEventListener('DOMContentLoaded', function() {
  const inputFecha = document.querySelector('input[name="fecha_vencimiento"]');
  
  if (inputFecha) {
    const hoy = new Date();
    hoy.setDate(hoy.getDate() + 1); // no permite hoy ni fechas anteriores

    const yyyy = hoy.getFullYear();
    const mm = String(hoy.getMonth() + 1).padStart(2, '0');
    const dd = String(hoy.getDate()).padStart(2, '0');

    const fechaMinima = `${yyyy}-${mm}-${dd}`;
    inputFecha.min = fechaMinima;
  }
});
