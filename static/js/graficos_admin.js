
// Configuración común para tooltips mejorados
const tooltipConfig = {
    backgroundColor: 'rgba(0,0,0,0.9)',
    titleColor: 'white',
    bodyColor: 'white',
    borderColor: 'rgba(255,255,255,0.2)',
    borderWidth: 1,
    cornerRadius: 8,
    displayColors: true,
    padding: 12,
    titleFont: { size: 14, weight: 'bold' },
    bodyFont: { size: 13 }
};

// Usuarios por Rol - Gráfico de dona mejorado
new Chart(document.getElementById('usuariosRol'), {
    type: 'doughnut',
    data: {
        labels: {{ roles_labels| safe }},
    datasets: [{
        data: {{ roles_data| safe }},
    backgroundColor: ['#667eea', '#f093fb', '#4facfe'],
    borderColor: ['#667eea', '#f093fb', '#4facfe'],
    borderWidth: 3,
    hoverBorderWidth: 5,
    hoverOffset: 15
                }]
            },
    options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'bottom',
            labels: {
                padding: 20,
                usePointStyle: true,
                font: { size: 12, weight: '500' }
            }
        },
        tooltip: {
            ...tooltipConfig,
            callbacks: {
                label: function (context) {
                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                    const percentage = ((context.parsed / total) * 100).toFixed(1);
                    return context.label + ': ' + context.parsed + ' (' + percentage + '%)';
                }
            }
        },
        title: {
            display: true,
            text: 'Distribución de Usuarios por Rol',
            font: { size: 16, weight: 'bold' },
            padding: { top: 10, bottom: 30 }
        }
    },
    animation: {
        animateScale: true,
        animateRotate: true,
        duration: 2000,
        easing: 'easeInOutQuart'
    },
    cutout: '65%'
}
        });

// Donaciones - Gráfico de barras mejorado
new Chart(document.getElementById('donaciones'), {
    type: 'bar',
    data: {
        labels: {{ donaciones_labels| safe }},
    datasets: [{
        label: 'Cantidad de Donaciones',
        data: {{ donaciones_data| safe }},
    backgroundColor: ['#667eea', '#f093fb'],
    borderColor: ['#667eea', '#f093fb'],
    borderWidth: 2,
    borderRadius: 8,
    borderSkipped: false,
    hoverBorderWidth: 3
                }]
            },
    options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: false
        },
        tooltip: {
            ...tooltipConfig,
            callbacks: {
                label: function (context) {
                    return 'Donaciones: ' + context.parsed.y;
                }
            }
        },
        title: {
            display: true,
            text: 'Donaciones Recibidas',
            font: { size: 16, weight: 'bold' },
            padding: { top: 10, bottom: 30 }
        }
    },
    scales: {
        y: {
            beginAtZero: true,
            grid: { color: 'rgba(0,0,0,0.05)' },
            ticks: {
                stepSize: 1,
                font: { weight: '500' }
            }
        },
        x: {
            grid: { display: false },
            ticks: {
                font: { weight: '500' }
            }
        }
    },
    animation: {
        duration: 2000,
        easing: 'easeInOutQuart',
        delay: function (context) {
            return context.dataIndex * 200;
        }
    }
}
        });

// Insumos por vencer - Gráfico horizontal mejorado
new Chart(document.getElementById('insumos'), {
    type: 'bar',
    data: {
        labels: {{ insumos_labels| safe }},
    datasets: [{
        label: 'Cantidad Disponible',
        data: {{ insumos_data| safe }},
    backgroundColor: '#ff9a9e',
    borderColor: '#ff9a9e',
    borderWidth: 2,
    borderRadius: 6,
    hoverBorderWidth: 3,
    hoverBackgroundColor: '#ff6b6b'
                }]
            },
    options: {
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: false
        },
        tooltip: {
            ...tooltipConfig,
            callbacks: {
                label: function (context) {
                    return 'Disponible: ' + context.parsed.x + ' unidades';
                }
            }
        },
        title: {
            display: true,
            text: 'Insumos por Vencer',
            font: { size: 16, weight: 'bold' },
            padding: { top: 10, bottom: 30 }
        }
    },
    scales: {
        x: {
            beginAtZero: true,
            grid: { color: 'rgba(0,0,0,0.05)' },
            ticks: {
                stepSize: 5,
                font: { weight: '500' }
            }
        },
        y: {
            grid: { display: false },
            ticks: {
                font: { weight: '500' }
            }
        }
    },
    animation: {
        duration: 2000,
        easing: 'easeInOutQuart',
        delay: function (context) {
            return context.dataIndex * 150;
        }
    }
}
        });

// Medicamentos por vencer - Gráfico horizontal mejorado con selector
const medicamentosData = {{ medicamentos_alerta| tojson | safe }};
let currentMedicamentoFilter = '';

// Poblar el selector de medicamentos
const medicamentoSelector = document.getElementById('medicamentoSelector');
const uniqueMedicamentos = [...new Set(medicamentosData.map(m => m.nombre_medicamento))];
uniqueMedicamentos.forEach(med => {
    const option = document.createElement('option');
    option.value = med;
    option.textContent = med;
    medicamentoSelector.appendChild(option);
});

const ctxMed = document.getElementById('chartMedicamentosVencer').getContext('2d');
let chartMedicamentos = new Chart(ctxMed, {
    type: 'bar',
    data: {
        labels: {{ medicamentos_labels| safe }},
datasets: [{
    label: 'Existencia',
    data: {{ medicamentos_data| safe }},
    backgroundColor: '#667eea',
    borderColor: '#667eea',
    borderWidth: 2,
    borderRadius: 6,
    hoverBorderWidth: 3,
    hoverBackgroundColor: '#764ba2'
                }]
            },
options: {
    indexAxis: 'y',
        responsive: true,
            maintainAspectRatio: false,
                plugins: {
        legend: {
            display: false
        },
        tooltip: {
                        ...tooltipConfig,
                callbacks: {
                label: function(context) {
                    const data = medicamentosData[context.dataIndex];
                    return [
                        'Existencia: ' + context.parsed.x + ' unidades',
                        'Lote: ' + data.lote,
                        'Vence: ' + new Date(data.fecha_vencimiento).toLocaleDateString('es-ES')
                    ];
                }
            }
        },
        title: {
            display: true,
                text: 'Medicamentos Próximos a Vencer',
                    font: { size: 16, weight: 'bold' },
            padding: { top: 10, bottom: 30 }
        }
    },
    scales: {
        x: {
            beginAtZero: true,
                grid: { color: 'rgba(0,0,0,0.05)' },
            ticks: {
                stepSize: 5,
                    font: { weight: '500' }
            }
        },
        y: {
            grid: { display: false },
            ticks: {
                font: { weight: '500' },
                maxTicksLimit: 10
            }
        }
    },
    animation: {
        duration: 2000,
            easing: 'easeInOutQuart',
                delay: function(context) {
                    return context.dataIndex * 150;
                }
    }
}
        });

// Función para filtrar medicamentos
function filterMedicamentos() {
    let filteredData = medicamentosData;
    if (currentMedicamentoFilter) {
        filteredData = medicamentosData.filter(m => m.nombre_medicamento === currentMedicamentoFilter);
    }

    const labels = filteredData.map(m => m.display_name);
    const data = filteredData.map(m => m.existencia);

    chartMedicamentos.data.labels = labels;
    chartMedicamentos.data.datasets[0].data = data;
    chartMedicamentos.update();

    // Actualizar lista detallada
    updateMedicamentosList(filteredData);
}

// Event listener para el selector
medicamentoSelector.addEventListener('change', function () {
    currentMedicamentoFilter = this.value;
    filterMedicamentos();
});

// Función para actualizar la lista detallada
function updateMedicamentosList(data) {
    const listContainer = document.getElementById('medicamentosDetailList');
    listContainer.innerHTML = '';

    if (data.length === 0) {
        listContainer.innerHTML = '<p class="text-muted">No hay medicamentos que cumplan con el filtro.</p>';
        return;
    }

    data.forEach(med => {
        const item = document.createElement('div');
        item.className = 'medicamento-item';
        item.style.cssText = 'padding: 8px; margin: 4px 0; background: rgba(102, 126, 234, 0.1); border-radius: 4px; border-left: 3px solid #667eea;';
        item.innerHTML = `
                    <strong>${med.nombre_medicamento}</strong><br>
                    <small class="text-muted">
                        Lote: ${med.lote} |
                        Existencia: ${med.existencia} |
                        Vence: ${new Date(med.fecha_vencimiento).toLocaleDateString('es-ES')}
                    </small>
                `;
        listContainer.appendChild(item);
    });
}

// Toggle para mostrar/ocultar lista detallada
document.getElementById('toggleListBtn').addEventListener('click', function () {
    const listDiv = document.getElementById('medicamentosList');
    const isVisible = listDiv.style.display !== 'none';

    if (isVisible) {
        listDiv.style.display = 'none';
        this.innerHTML = '<i class="fas fa-list"></i> Ver Lista Detallada';
    } else {
        listDiv.style.display = 'block';
        this.innerHTML = '<i class="fas fa-list-ul"></i> Ocultar Lista';
        updateMedicamentosList(currentMedicamentoFilter ?
            medicamentosData.filter(m => m.nombre_medicamento === currentMedicamentoFilter) :
            medicamentosData);
    }
});

// Inicializar lista detallada
updateMedicamentosList(medicamentosData);

// Funcionalidad del modal de usuarios
let usuariosData = [];
let currentUsuariosPage = 1;
let registrosPorPaginaUsuarios = 5;
let filteredUsuariosData = [];
let sortUsuariosColumn = -1;
let sortUsuariosDirection = 'asc';

// Función para abrir modal de usuarios
window.abrirModalUsuarios = function () {
    // Obtener datos de usuarios desde el servidor
    fetch('/api/usuarios')
        .then(response => response.json())
        .then(data => {
            usuariosData = data;
            filteredUsuariosData = [...usuariosData];
            currentUsuariosPage = 1;
            document.getElementById('usuariosModal').style.display = 'block';
            renderUsuariosTable();
            renderUsuariosPagination();
            updateUsuariosSortIcons();
        })
        .catch(error => {
            console.error('Error al cargar usuarios:', error);
            alert('Error al cargar la lista de usuarios');
        });
};

// Función para cerrar modal de usuarios
window.cerrarModalUsuarios = function () {
    document.getElementById('usuariosModal').style.display = 'none';
};

// Cerrar modal al hacer clic fuera
window.onclick = function (event) {
    const modal = document.getElementById('usuariosModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};

// Función de búsqueda de usuarios
document.getElementById('searchUsuarios').addEventListener('input', function () {
    const searchTerm = this.value.toLowerCase();
    filteredUsuariosData = usuariosData.filter(usuario =>
        usuario.numero_documento.toString().includes(searchTerm) ||
        usuario.nombre_usuario.toLowerCase().includes(searchTerm) ||
        usuario.apellido_usuario.toLowerCase().includes(searchTerm) ||
        usuario.tipo_documento_usuario.toLowerCase().includes(searchTerm) ||
        usuario.correo_electronico_usuario.toLowerCase().includes(searchTerm) ||
        usuario.telefono.toLowerCase().includes(searchTerm) ||
        usuario.nombre_rol.toLowerCase().includes(searchTerm)
    );
    currentUsuariosPage = 1;
    renderUsuariosTable();
    renderUsuariosPagination();
});

// Función de ordenamiento de usuarios
document.querySelectorAll('#usuariosTable th.sortable').forEach(header => {
    header.addEventListener('click', function () {
        const column = parseInt(this.dataset.column);
        if (sortUsuariosColumn === column) {
            sortUsuariosDirection = sortUsuariosDirection === 'asc' ? 'desc' : 'asc';
        } else {
            sortUsuariosColumn = column;
            sortUsuariosDirection = 'asc';
        }
        sortUsuariosData();
        renderUsuariosTable();
        updateUsuariosSortIcons();
    });
});

function sortUsuariosData() {
    filteredUsuariosData.sort((a, b) => {
        let aVal = Object.values(a)[sortUsuariosColumn];
        let bVal = Object.values(b)[sortUsuariosColumn];

        if (typeof aVal === 'string') {
            aVal = aVal.toLowerCase();
            bVal = bVal.toLowerCase();
        }

        if (sortUsuariosDirection === 'asc') {
            return aVal > bVal ? 1 : -1;
        } else {
            return aVal < bVal ? 1 : -1;
        }
    });
}

function updateUsuariosSortIcons() {
    document.querySelectorAll('#usuariosTable th.sortable i').forEach((icon, index) => {
        if (index === sortUsuariosColumn) {
            icon.className = sortUsuariosDirection === 'asc' ? 'fas fa-sort-up' : 'fas fa-sort-down';
        } else {
            icon.className = 'fas fa-sort';
        }
    });
}

// Cambio de registros por página
document.getElementById('registrosPorPaginaUsuarios').addEventListener('change', function () {
    registrosPorPaginaUsuarios = parseInt(this.value);
    currentUsuariosPage = 1;
    renderUsuariosTable();
    renderUsuariosPagination();
});

function renderUsuariosTable() {
    const startIndex = (currentUsuariosPage - 1) * registrosPorPaginaUsuarios;
    const endIndex = startIndex + registrosPorPaginaUsuarios;
    const pageData = filteredUsuariosData.slice(startIndex, endIndex);

    let html = '';
    if (pageData.length === 0) {
        html = '<tr><td colspan="7" class="text-center">No se encontraron resultados.</td></tr>';
    } else {
        pageData.forEach(usuario => {
            html += `
                        <tr>
                            <td>${usuario.numero_documento}</td>
                            <td>${usuario.nombre_usuario}</td>
                            <td>${usuario.apellido_usuario}</td>
                            <td>${usuario.tipo_documento_usuario}</td>
                            <td>${usuario.correo_electronico_usuario}</td>
                            <td>${usuario.telefono || 'N/A'}</td>
                            <td>${usuario.nombre_rol}</td>
                        </tr>
                    `;
        });
    }

    document.getElementById('usuariosTableBody').innerHTML = html;

    // Actualizar información de registros
    const totalRegistros = filteredUsuariosData.length;
    const inicio = totalRegistros === 0 ? 0 : startIndex + 1;
    const fin = Math.min(endIndex, totalRegistros);
    document.getElementById('usuariosPaginationInfo').textContent = `Mostrando ${inicio} - ${fin} de ${totalRegistros} registros`;
}

function renderUsuariosPagination() {
    const totalPages = Math.ceil(filteredUsuariosData.length / registrosPorPaginaUsuarios);
    const paginationNav = document.getElementById('usuariosPaginationNav');
    const pageNumbers = document.getElementById('usuariosPageNumbers');

    if (totalPages > 1) {
        paginationNav.style.display = 'flex';
        let html = '';

        for (let i = 1; i <= totalPages; i++) {
            if (i === currentUsuariosPage) {
                html += `<button class="usuarios-page-number usuarios-page-btn active">${i}</button>`;
            } else {
                html += `<button class="usuarios-page-number usuarios-page-btn" onclick="changeUsuariosPage(${i})">${i}</button>`;
            }
        }

        pageNumbers.innerHTML = html;
    } else {
        paginationNav.style.display = 'none';
    }

    // Actualizar botones anterior/siguiente
    document.getElementById('usuariosPrevPage').disabled = currentUsuariosPage === 1;
    document.getElementById('usuariosNextPage').disabled = currentUsuariosPage === totalPages;
}

window.changeUsuariosPage = function (page) {
    currentUsuariosPage = page;
    renderUsuariosTable();
    renderUsuariosPagination();
};

// Event listeners para navegación de usuarios
document.getElementById('usuariosPrevPage').addEventListener('click', function () {
    if (currentUsuariosPage > 1) {
        changeUsuariosPage(currentUsuariosPage - 1);
    }
});

document.getElementById('usuariosNextPage').addEventListener('click', function () {
    const totalPages = Math.ceil(filteredUsuariosData.length / registrosPorPaginaUsuarios);
    if (currentUsuariosPage < totalPages) {
        changeUsuariosPage(currentUsuariosPage + 1);
    }
});

// Funcionalidad del modal de reportes
const modal = document.getElementById('reporteModal');
const closeBtn = document.getElementsByClassName('close')[0];
const generarBtn = document.getElementById('generarReporteBtn');
const imprimirBtn = document.getElementById('imprimirBtn');

// Cerrar modal
closeBtn.onclick = function () {
    modal.style.display = 'none';
}

// Cerrar modal al hacer clic fuera
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

// Event listener para mostrar/ocultar subtipo de donaciones
document.getElementById('tipo_reporte').addEventListener('change', function () {
    const subtipoGroup = document.getElementById('subtipoDonacionesGroup');
    if (this.value === 'donaciones') {
        subtipoGroup.style.display = 'block';
    } else {
        subtipoGroup.style.display = 'none';
        document.getElementById('subtipo_donaciones').value = '';
    }
});

// Generar reporte
generarBtn.onclick = function () {
    const tipoReporte = document.getElementById('tipo_reporte').value;
    const subtipoDonaciones = document.getElementById('subtipo_donaciones').value;
    const fechaInicio = document.getElementById('fecha_inicio').value;
    const fechaFin = document.getElementById('fecha_fin').value;

    if (!tipoReporte || !fechaInicio || !fechaFin) {
        alert('Por favor complete todos los campos');
        return;
    }

    // Mostrar loading
    generarBtn.disabled = true;
    generarBtn.textContent = 'Generando...';

    // Preparar datos para enviar
    const formData = {
        tipo_reporte: tipoReporte,
        fecha_inicio: fechaInicio,
        fecha_fin: fechaFin
    };

    if (tipoReporte === 'donaciones' && subtipoDonaciones) {
        formData.subtipo_donaciones = subtipoDonaciones;
    }

    // Enviar petición AJAX
    fetch('/generar_reporte', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams(formData)
    })
        .then(response => response.json())
        .then(data => {
            mostrarReporteEnModal(data);
            modal.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al generar el reporte');
        })
        .finally(() => {
            generarBtn.disabled = false;
            generarBtn.textContent = 'Generar Reporte';
        });
}

// Event listeners para paginación
document.getElementById('registrosPorPagina').addEventListener('change', function () {
    registrosPorPagina = parseInt(this.value);
    currentPage = 1;
    actualizarPaginacion();
    mostrarPaginaActual();
});

document.getElementById('prevPage').addEventListener('click', function () {
    if (currentPage > 1) {
        cambiarPagina(currentPage - 1);
    }
});

document.getElementById('nextPage').addEventListener('click', function () {
    const totalPaginas = Math.ceil(datosActuales.length / registrosPorPagina);
    if (currentPage < totalPaginas) {
        cambiarPagina(currentPage + 1);
    }
});

// Variables globales para paginación
let currentPage = 1;
let registrosPorPagina = 5;
let datosActuales = [];

// Función para mostrar el reporte en el modal
function mostrarReporteEnModal(data) {
    document.getElementById('modalTitle').textContent = data.titulo;
    datosActuales = data.datos;
    currentPage = 1;

    const registrosSelect = document.getElementById('registrosPorPagina');
    registrosSelect.value = registrosPorPagina;

    actualizarPaginacion();
    mostrarPaginaActual();
}

// Función para actualizar la información de paginación
function actualizarPaginacion() {
    const totalRegistros = datosActuales.length;
    const totalPaginas = Math.ceil(totalRegistros / registrosPorPagina);

    // Actualizar información de registros
    const registrosInfo = document.getElementById('registrosInfo');
    if (totalRegistros === 0) {
        registrosInfo.textContent = 'No se encontraron registros';
    } else {
        const inicio = (currentPage - 1) * registrosPorPagina + 1;
        const fin = Math.min(currentPage * registrosPorPagina, totalRegistros);
        registrosInfo.textContent = `Mostrando ${inicio} - ${fin} de ${totalRegistros} registros`;
    }

    // Mostrar/ocultar navegación de páginas
    const paginationNav = document.getElementById('paginationNav');
    if (totalPaginas > 1) {
        paginationNav.style.display = 'flex';
        generarNumerosPaginas(totalPaginas);
    } else {
        paginationNav.style.display = 'none';
    }

    // Actualizar botones anterior/siguiente
    document.getElementById('prevPage').disabled = currentPage === 1;
    document.getElementById('nextPage').disabled = currentPage === totalPaginas;
}

// Función para generar los números de página
function generarNumerosPaginas(totalPaginas) {
    const pageNumbers = document.getElementById('pageNumbers');
    pageNumbers.innerHTML = '';

    for (let i = 1; i <= totalPaginas; i++) {
        const pageBtn = document.createElement('button');
        pageBtn.className = 'page-number';
        pageBtn.textContent = i;
        if (i === currentPage) {
            pageBtn.classList.add('active');
        }
        pageBtn.onclick = () => cambiarPagina(i);
        pageNumbers.appendChild(pageBtn);
    }
}

// Función para cambiar de página
function cambiarPagina(pagina) {
    currentPage = pagina;
    mostrarPaginaActual();
    actualizarPaginacion();
}

// Función para mostrar la página actual
function mostrarPaginaActual() {
    const tableHead = document.getElementById('reporteTableHead');
    const tableBody = document.getElementById('reporteTableBody');
    const noDataMessage = document.getElementById('noDataMessage');
    const reporteTable = document.getElementById('reporteTable');

    // Limpiar tabla anterior
    tableHead.innerHTML = '';
    tableBody.innerHTML = '';

    if (datosActuales.length === 0) {
        reporteTable.style.display = 'none';
        noDataMessage.style.display = 'block';
        return;
    }

    reporteTable.style.display = 'table';
    noDataMessage.style.display = 'none';

    // Calcular índices para la página actual
    const inicio = (currentPage - 1) * registrosPorPagina;
    const fin = Math.min(inicio + registrosPorPagina, datosActuales.length);
    const datosPagina = datosActuales.slice(inicio, fin);

    // Crear encabezados según el tipo de reporte
    const headers = [];
    if (datosActuales.length > 0 && datosActuales[0].hasOwnProperty('fecha_adopcion')) {
        headers.push('Fecha de Adopción', 'Animal Adoptado', 'Adoptante');
    } else if (datosActuales.length > 0 && datosActuales[0].hasOwnProperty('tipo')) {
        headers.push('Tipo', 'Fecha de Donación', 'Descripción', 'Cantidad', 'Unidad');
    } else if (datosActuales.length > 0 && datosActuales[0].hasOwnProperty('fecha_consulta')) {
        headers.push('Fecha', 'Hora', 'Paciente', 'Estado', 'Diagnóstico');
    }

    // Crear fila de encabezados
    const headerRow = document.createElement('tr');
    headers.forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
    });
    tableHead.appendChild(headerRow);

    // Crear filas de datos para la página actual
    datosPagina.forEach(dato => {
        const row = document.createElement('tr');

        if (dato.hasOwnProperty('fecha_adopcion')) {
            row.innerHTML = `
                        <td>${dato.fecha_adopcion}</td>
                        <td>${dato.nombre_temporal}</td>
                        <td>${dato.adoptante_nombre}</td>
                    `;
        } else if (dato.hasOwnProperty('tipo')) {
            row.innerHTML = `
                        <td>${dato.tipo}</td>
                        <td>${dato.fecha_donacion}</td>
                        <td>${dato.descripcion}</td>
                        <td>${dato.cantidad}</td>
                        <td>${dato.unidad_medida}</td>
                    `;
        } else if (dato.hasOwnProperty('fecha_consulta')) {
            row.innerHTML = `
                        <td>${dato.fecha_consulta}</td>
                        <td>${dato.hora_consulta}</td>
                        <td>${dato.nombre_paciente}</td>
                        <td>${dato.estado_consulta}</td>
                        <td>${dato.diagnostico || 'N/A'}</td>
                    `;
        }

        tableBody.appendChild(row);
    });
}

// Función de impresión del modal
imprimirBtn.onclick = function () {
    // Crear una ventana de impresión con solo el contenido del modal
    const printWindow = window.open('', '_blank');

    // Obtener el título del modal
    const titulo = document.getElementById('modalTitle').textContent;

    // Crear tabla completa con todos los datos (sin paginación)
    let tableHTML = '<table>';
    const headers = [];

    // Determinar headers según el tipo de reporte
    if (datosActuales.length > 0) {
        if (datosActuales[0].hasOwnProperty('fecha_adopcion')) {
            headers.push('Fecha de Adopción', 'Animal Adoptado', 'Adoptante');
        } else if (datosActuales[0].hasOwnProperty('tipo')) {
            headers.push('Tipo', 'Fecha de Donación', 'Descripción', 'Cantidad', 'Unidad');
        } else if (datosActuales[0].hasOwnProperty('fecha_consulta')) {
            headers.push('Fecha', 'Hora', 'Paciente', 'Estado', 'Diagnóstico');
        }
    }

    // Crear fila de encabezados
    tableHTML += '<thead><tr>';
    headers.forEach(header => {
        tableHTML += `<th>${header}</th>`;
    });
    tableHTML += '</tr></thead><tbody>';

    // Crear todas las filas de datos (sin paginación)
    datosActuales.forEach(dato => {
        tableHTML += '<tr>';
        if (dato.hasOwnProperty('fecha_adopcion')) {
            tableHTML += `
                        <td>${dato.fecha_adopcion}</td>
                        <td>${dato.nombre_temporal}</td>
                        <td>${dato.adoptante_nombre}</td>
                    `;
        } else if (dato.hasOwnProperty('tipo')) {
            tableHTML += `
                        <td>${dato.tipo}</td>
                        <td>${dato.fecha_donacion}</td>
                        <td>${dato.descripcion}</td>
                        <td>${dato.cantidad}</td>
                        <td>${dato.unidad_medida}</td>
                    `;
        } else if (dato.hasOwnProperty('fecha_consulta')) {
            tableHTML += `
                        <td>${dato.fecha_consulta}</td>
                        <td>${dato.hora_consulta}</td>
                        <td>${dato.nombre_paciente}</td>
                        <td>${dato.estado_consulta}</td>
                        <td>${dato.diagnostico || 'N/A'}</td>
                    `;
        }
        tableHTML += '</tr>';
    });
    tableHTML += '</tbody></table>';

    // Crear el contenido HTML para impresión
    const printContent = `
                <!DOCTYPE html>
                <html lang="es">
                <head>
                    <meta charset="UTF-8">
                    <title>${titulo}</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            margin: 20px;
                            color: #333;
                            position: relative;
                        }
                        .logo-background {
                            position: fixed;
                            top: 50%;
                            left: 50%;
                            transform: translate(-50%, -50%);
                            width: 700px;
                            height: auto;
                            opacity: 0.50;
                            z-index: 0;
                            pointer-events: none;
                        }
                        .content-wrapper {
                            position: relative;
                            z-index: 1;
                        }
                        .header-print {
                            text-align: center;
                            margin-bottom: 30px;
                            border-bottom: 2px solid #333;
                            padding-bottom: 20px;
                        }
                        .title-print {
                            font-size: 24px;
                            font-weight: bold;
                            color: #333;
                            margin: 10px 0;
                        }
                        .date-print {
                            font-size: 14px;
                            color: #666;
                            margin-bottom: 20px;
                        }
                        table {
                            width: 100%;
                            border-collapse: collapse;
                            margin-top: 20px;
                            font-size: 12px;
                        }
                        th, td {
                            border: 1px solid #ddd;
                            padding: 8px;
                            text-align: left;
                        }
                        th {
                            background-color: #f8f9fa;
                            font-weight: bold;
                            text-align: center;
                        }
                        tr:nth-child(even) {
                            background-color: #f9f9f9;
                        }
                        .footer-print {
                            margin-top: 30px;
                            text-align: center;
                            font-size: 10px;
                            color: #666;
                            border-top: 1px solid #ddd;
                            padding-top: 10px;
                        }
                        @media print {
                            body { margin: 0; }
                            .no-print { display: none; }
                        }
                    </style>
                </head>
                <body>
                    <img src="/static/img/patitas2.png" alt="PetFriendly Logo" class="logo-background">

                    <div class="content-wrapper">
                        <div class="header-print">
                            <div class="title-print">${titulo}</div>
                            <div class="date-print">Generado el ${new Date().toLocaleDateString('es-ES')}</div>
                        </div>

                        ${tableHTML}

                        <div class="footer-print">
                            Reporte generado por PetFriendly - ${new Date().toLocaleString('es-ES')}
                        </div>
                    </div>
                </body>
                </html>
            `;

    printWindow.document.write(printContent);
    printWindow.document.close();

    // Esperar a que se cargue la imagen antes de imprimir
    printWindow.onload = function () {
        printWindow.print();
        printWindow.close();
    };
}