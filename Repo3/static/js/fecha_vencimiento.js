  // 📅 Fecha actual
const hoy = new Date();
const yyyy = hoy.getFullYear();
const mm = String(hoy.getMonth() + 1).padStart(2, '0');
const dd = String(hoy.getDate()).padStart(2, '0');
const fechaHoy = `${yyyy}-${mm}-${dd}`;

// 🔹 Fecha de donación: solo hoy o fechas pasadas
const inputDonacion = document.getElementById('fecha_donacion');
if (inputDonacion) {
  inputDonacion.max = fechaHoy;
}

// 🔹 Fecha de vencimiento: solo hoy o fechas futuras
const inputVencimiento = document.getElementById('fecha_vencimiento');
if (inputVencimiento) {
  inputVencimiento.min = fechaHoy;
}
