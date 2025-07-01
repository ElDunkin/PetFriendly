// Cambia URL si tu backend no está en localhost:5000
const API_URL = "http://localhost:5000/api";

if (document.getElementById("loginForm")) {
  document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;
    try {
      const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      if (res.ok) {
        localStorage.setItem("token", data.token);
        localStorage.setItem("nombre", data.nombre);
        window.location.href = "dashboard.html";
      } else {
        document.getElementById("loginError").textContent = data.message;
      }
    } catch (err) {
      document.getElementById("loginError").textContent = "Error de conexión";
    }
  });
}

/* if (document.getElementById("registerForm")) {
  document.getElementById("registerForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const nombre = document.getElementById("regNombre").value;
    const email = document.getElementById("regEmail").value;
    const password = document.getElementById("regPassword").value;
    try {
      const res = await fetch(`${API_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre, email, password }),
      });
      const data = await res.json();
      if (res.ok) {
        alert("Registro exitoso, ahora inicia sesión");
        window.location.href = "index.html";
      } else {
        document.getElementById("registerError").textContent = data.message;
      }
    } catch (err) {
      document.getElementById("registerError").textContent = "Error de conexión";
    }
  });
}
 */
if (window.location.pathname.endsWith("dashboard_clientes.html")) {
  async function cargarDashboard() {
    const token = localStorage.getItem("token");
    if (!token) {
      window.location.href = "index_clientes.html";
      return;
    }
    try {
      const res = await fetch(`${API_URL}/dashboard_clientes`, {
        headers: { "Authorization": "Bearer " + token }
      });
      const data = await res.json();
      if (res.ok) {
        document.getElementById("welcomeMsg").textContent = data.message;
      } else {
        localStorage.removeItem("token");
        window.location.href = "index_clientes.html";
      }
    } catch (err) {
      document.getElementById("welcomeMsg").textContent = "Error al cargar el dashboard";
    }
  }
  cargarDashboard();
}

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("nombre");
  window.location.href = "index_clientes.html";
}