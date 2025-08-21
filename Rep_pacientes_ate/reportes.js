let datosReporte = [];

const tablaPacientes = document.querySelector("#tabla-pacientes tbody");
const btnPDF = document.getElementById("btn-pdf");
const btnExcel = document.getElementById("btn-excel");
const errorFiltros = document.getElementById("error-filtros");
const filtrosForm = document.getElementById("filtros-form");

filtrosForm.onsubmit = async function(e) {
    e.preventDefault();
    errorFiltros.textContent = "";
    tablaPacientes.innerHTML = "";
    btnPDF.disabled = true;
    btnExcel.disabled = true;

    const form = e.target;
    const filtros = {
        fecha_inicio: form.fecha_inicio.value,
        fecha_fin: form.fecha_fin.value,
        tipo_servicio: form.tipo_servicio.value
    };

    if (!filtros.fecha_inicio && !filtros.tipo_servicio) {
        errorFiltros.textContent = "Debe seleccionar al menos un filtro.";
        return;
    }
    if (filtros.fecha_inicio && filtros.fecha_fin && filtros.fecha_inicio > filtros.fecha_fin) {
        errorFiltros.textContent = "La fecha de inicio debe ser anterior a la fecha de fin.";
        return;
    }

    try {
        const resp = await fetch("/api/reporte_pacientes", {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify(filtros)
        });
        if (!resp.ok) {
            const err = await resp.json();
            errorFiltros.textContent = err.error || "Error al obtener datos.";
            return;
        }
        datosReporte = await resp.json();
        if (datosReporte.length === 0) {
            tablaPacientes.innerHTML = "<tr><td colspan='7'>No hay datos para los filtros seleccionados.</td></tr>";
            btnPDF.disabled = true;
            btnExcel.disabled = true;
        } else {
            tablaPacientes.innerHTML = datosReporte.map(row =>
                `<tr>
                    <td>${row.paciente}</td>
                    <td>${row.propietario}</td>
                    <td>${row.fecha_consulta}</td>
                    <td>${row.medico}</td>
                    <td>${row.tipo_servicio}</td>
                    <td>${row.diagnostico}</td>
                    <td>${row.estado}</td>
                </tr>`
            ).join("");
            btnPDF.disabled = false;
            btnExcel.disabled = false;
        }
    } catch {
        errorFiltros.textContent = "Error al consultar el reporte.";
    }
};

// Exportar CSV
btnPDF.onclick = function() {
    if (datosReporte.length === 0) return;
    fetch("/api/exportar_reporte", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ pacientes: datosReporte, formato: "csv" })
    }).then(async resp => {
        if (!resp.ok) {
            alert("Error al exportar el archivo.");
            return;
        }
        const blob = await resp.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        let fname = resp.headers.get("Content-Disposition")?.split("filename=")[1]?.replaceAll('"', '') || "reporte.csv";
        a.href = url;
        a.download = fname;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    });
};

// Exportar Excel
btnExcel.onclick = function() {
    if (datosReporte.length === 0) return;
    fetch("/api/exportar_reporte", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ pacientes: datosReporte, formato: "excel" })
    }).then(async resp => {
        if (!resp.ok) {
            alert("Error al exportar el archivo.");
            return;
        }
        const blob = await resp.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        let fname = resp.headers.get("Content-Disposition")?.split("filename=")[1]?.replaceAll('"', '') || "reporte.xlsx";
        a.href = url;
        a.download = fname;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    });
};