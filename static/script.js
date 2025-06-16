document.getElementById('loginForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const usuario = document.getElementById('usuario').value;
  const password = document.getElementById('password').value;

  const res = await fetch('/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ usuario, password }),
  });

  const data = await res.json();
  if (data.success) {
    alert('Inicio de sesión exitoso');
    window.location.href = '/dashboard'; // puedes personalizar esto
  } else {
    alert('Credenciales incorrectas');
  }
});
