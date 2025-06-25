document.getElementById('btn-add-pet').addEventListener('click', function() {
    // Abre modal o formulario para agregar mascota
    alert("Funcionalidad de agregar mascota");
});

function verHistorial(petId) {
    // Redirige o muestra historial médico de la mascota
    alert("Ver historial de mascota: " + petId);
}
function openModal(modalId) {
  document.getElementById(modalId).style.display = "flex";
}
function closeModal(modalId) {
  document.getElementById(modalId).style.display = "none";
}

function showPetHistory(petId) {
  fetch("/api/pet_history/" + petId)
    .then(res => res.json())
    .then(data => {
      let html = "";
      if(!data.history || data.history.length === 0) {
        html = "<p>No hay historial disponible.</p>";
      } else {
        html = "<ul>";
        data.history.forEach(item => {
          html += `<li>${item.fecha}: ${item.descripcion}</li>`;
        });
        html += "</ul>";
      }
      document.getElementById("petHistoryContent").innerHTML = html;
      openModal('modalPetHistory');
    });
}