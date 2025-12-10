document.addEventListener("DOMContentLoaded", function () {
    const tabla = document.getElementById("tablaUsuarios");
    if (!tabla) return console.error("No se encontró #tablaUsuarios");

    const tbody = tabla.querySelector("tbody");
    const filtroInput = document.getElementById("filtro");
    const paginacionDiv = document.getElementById("paginacion");
    const headers = Array.from(tabla.querySelectorAll("th[data-col]"));

    // Config
    let rowsAll = Array.from(tbody.querySelectorAll("tr")); // todas las filas originales (nodos DOM)
    let rowsFiltered = rowsAll.slice(); // filas activas (filtrado/ordenado)
    let currentPage = 1;
    const rowsPerPage = 3; // <- cambia esto si quieres otro tamaño de página
    const sortState = { col: null, asc: true };

    function renderTablePage(page = 1) {
        tbody.innerHTML = "";
        if (rowsFiltered.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center">No se encontraron registros.</td></tr>';
            paginacionDiv.innerHTML = "";
            return;
        }

        const totalPages = Math.max(1, Math.ceil(rowsFiltered.length / rowsPerPage));
        if (page < 1) page = 1;
        if (page > totalPages) page = totalPages;
        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        rowsFiltered.slice(start, end).forEach(r => tbody.appendChild(r));
        currentPage = page;
        renderPagination(totalPages);
    }

    function renderPagination(totalPages) {
        paginacionDiv.innerHTML = "";

        // Mostrar paginación solo si hay más filas que rowsPerPage
        if (rowsFiltered.length <= rowsPerPage) return;

        const createBtn = (label, cls = "") => {
            const b = document.createElement("button");
            b.type = "button";
            b.className = "btn btn-sm me-1 " + cls;
            b.textContent = label;
            return b;
        };

        // Prev
        const prev = createBtn("«", currentPage === 1 ? "btn-secondary disabled" : "btn-outline-primary");
        prev.addEventListener("click", () => renderTablePage(currentPage - 1));
        paginacionDiv.appendChild(prev);

        // Números
        for (let i = 1; i <= totalPages; i++) {
            const isActive = i === currentPage;
            const btn = createBtn(i, isActive ? "btn-primary" : "btn-outline-primary");
            btn.addEventListener("click", () => renderTablePage(i));
            paginacionDiv.appendChild(btn);
        }

        // Next
        const next = createBtn("»", currentPage === totalPages ? "btn-secondary disabled" : "btn-outline-primary");
        next.addEventListener("click", () => renderTablePage(currentPage + 1));
        paginacionDiv.appendChild(next);
    }

    // Ordenamiento por columna
    headers.forEach(h => {
        h.style.cursor = "pointer";
        const colIndex = Number(h.dataset.col);
        const icon = document.createElement("span");
        icon.className = "ms-1";
        h.appendChild(icon);

        h.addEventListener("click", () => {
            if (sortState.col === colIndex) sortState.asc = !sortState.asc;
            else { sortState.col = colIndex; sortState.asc = true; }

            rowsFiltered.sort((a, b) => {
                const aText = (a.children[colIndex]?.textContent || "").trim().toLowerCase();
                const bText = (b.children[colIndex]?.textContent || "").trim().toLowerCase();

                // Intentar comparación numérica
                const aNum = parseFloat(aText.replace(/[^\d\-,.\s]/g, "").replace(",", "."));
                const bNum = parseFloat(bText.replace(/[^\d\-,.\s]/g, "").replace(",", "."));
                if (!Number.isNaN(aNum) && !Number.isNaN(bNum) && aText !== "" && bText !== "") {
                    return sortState.asc ? aNum - bNum : bNum - aNum;
                } else {
                    if (aText < bText) return sortState.asc ? -1 : 1;
                    if (aText > bText) return sortState.asc ? 1 : -1;
                    return 0;
                }
            });

            // Mantener el nuevo orden global (útil si luego limpias filtro)
            rowsAll = rowsFiltered.slice();

            // Actualizar iconos
            headers.forEach(h2 => {
                const sp = h2.querySelector("span.ms-1");
                if (h2 === h) sp.textContent = sortState.asc ? "▲" : "▼";
                else if (sp) sp.textContent = "";
            });

            renderTablePage(1);
        });
    });

    // Filtrado global
    filtroInput.addEventListener("input", () => {
        const q = filtroInput.value.trim().toLowerCase();
        if (q === "") {
            rowsFiltered = rowsAll.slice();
        } else {
            rowsFiltered = rowsAll.filter(row => row.textContent.toLowerCase().includes(q));
        }
        renderTablePage(1);
    });

    // Inicializar
    renderTablePage(1);
});