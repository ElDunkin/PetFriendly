const inputFecha = document.getElementById('fecha_nacimiento_paciente');
  const hoy = new Date();
  const yyyy = hoy.getFullYear();
  const mm = String(hoy.getMonth() + 1).padStart(2, '0');
  const dd = String(hoy.getDate()).padStart(2, '0');
  inputFecha.max = `${yyyy}-${mm}-${dd}`