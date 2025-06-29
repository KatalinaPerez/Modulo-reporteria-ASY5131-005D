// main_api/static/js/DespaApi.js  <-- ¡¡¡CONFIRMADO EL NOMBRE 'DespaApi.js'!!!

document.addEventListener('DOMContentLoaded', function() {
    const tableBody = document.getElementById('despachos-table');
    const filterColumnSelect = document.getElementById('filter-column-despacho');
    const filterValueInput = document.getElementById('filter-value-despacho');
    const applyFilterButton = document.getElementById('apply-filter-despacho');
    const sortColumnSelect = document.getElementById('sort-column-despacho');
    const sortOrderSelect = document.getElementById('sort-order-despacho');
    const applySortButton = document.getElementById('apply-sort-despacho');

    let allDespachoData = [];

    async function fetchDespachoData() {
    try {
        // ¡¡¡CAMBIADO AQUÍ PARA BUSCAR 'despa_datos_mock.json'!!!
        const response = await fetch('/static/js/despa_datos_mock.json');

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status} (${response.statusText}) - Asegúrate que 'despa_datos_mock.json' está en main_api/static/js/`);
        }
        allDespachoData = await response.json();
        renderTable(allDespachoData);
    } catch (error) {
        console.error('Error fetching despacho data:', error);
        if (tableBody) {
            tableBody.innerHTML = '<tr><td colspan="6">Error al cargar los datos de despacho. Verifica la consola para más detalles.</td></tr>';
        }
    }
}

    function renderTable(data) {
        if (!tableBody) {
            console.error("Error: Elemento con ID 'despachos-table' no encontrado para renderizar en Despacho.");
            return;
        }
        tableBody.innerHTML = '';
        if (data.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="6">No hay registros de despacho para mostrar.</td></tr>';
            return;
        }
        data.forEach(item => {
            const row = tableBody.insertRow();
            // Los nombres de las propiedades del JSON coinciden directamente con las columnas de la tabla
            row.insertCell().textContent = item.idDespacho;
            row.insertCell().textContent = item.fecha; // Puedes formatear esta fecha si necesitas (ej. new Date(item.fecha).toLocaleDateString())
            row.insertCell().textContent = item.producto;
            row.insertCell().textContent = item.cantidad;
            row.insertCell().textContent = item.destinatario;
            row.insertCell().textContent = item.estado;
        });
    }

    function applyFiltersAndSort() {
        let filteredData = [...allDespachoData];

        if (filterColumnSelect && filterValueInput) {
            const filterColumn = filterColumnSelect.value;
            const filterValue = filterValueInput.value.toLowerCase();

            if (filterValue) {
                filteredData = filteredData.filter(item => {
                    let itemValue;
                    // Las opciones de filtro y ordenamiento ahora corresponden directamente a las claves del JSON
                    if (filterColumn === 'idDespacho') {
                        itemValue = item.idDespacho;
                    } else if (filterColumn === 'producto') {
                        itemValue = item.producto;
                    } else if (filterColumn === 'cantidad') {
                        itemValue = item.cantidad;
                    } else if (filterColumn === 'destinatario') {
                        itemValue = item.destinatario;
                    } else if (filterColumn === 'estado') {
                        itemValue = item.estado;
                    }
                    return itemValue && itemValue.toString().toLowerCase().includes(filterValue);
                });
            }
        } else {
            console.warn("Elementos de filtro no encontrados para Despacho, omitiendo filtrado.");
        }

        if (sortColumnSelect && sortOrderSelect) {
            const sortColumn = sortColumnSelect.value;
            const sortOrder = sortOrderSelect.value;

            filteredData.sort((a, b) => {
                let valA, valB;
                if (sortColumn === 'idDespacho') {
                    valA = a.idDespacho;
                    valB = b.idDespacho;
                } else if (sortColumn === 'fecha') {
                    valA = new Date(a.fecha);
                    valB = new Date(b.fecha);
                } else if (sortColumn === 'producto') {
                    valA = a.producto;
                    valB = b.producto;
                } else if (sortColumn === 'cantidad') {
                    valA = parseFloat(a.cantidad);
                    valB = parseFloat(b.cantidad);
                } else if (sortColumn === 'destinatario') {
                    valA = a.destinatario;
                    valB = b.destinatario;
                } else if (sortColumn === 'estado') {
                    valA = a.estado;
                    valB = b.estado;
                }

                if (typeof valA === 'number' && typeof valB === 'number') {
                    return sortOrder === 'asc' ? valA - valB : valB - valA;
                } else {
                    const comparison = String(valA || '').localeCompare(String(valB || ''));
                    return sortOrder === 'asc' ? comparison : -comparison;
                }
            });
        } else {
            console.warn("Elementos de ordenamiento no encontrados para Despacho, omitiendo ordenamiento.");
        }

        renderTable(filteredData);
    }

    if (applyFilterButton) {
        applyFilterButton.addEventListener('click', applyFiltersAndSort);
    } else {
        console.error("Error: Elemento con ID 'apply-filter-despacho' no encontrado para Despacho. Revisa tu Despacho.html");
    }

    if (applySortButton) {
        applySortButton.addEventListener('click', applyFiltersAndSort);
    } else {
        console.error("Error: Elemento con ID 'apply-sort-despacho' no encontrado para Despacho. Revisa tu Despacho.html");
    }

    if (filterValueInput) {
        filterValueInput.addEventListener('keyup', (event) => {
            if (event.key === 'Enter') {
                applyFiltersAndSort();
            }
        });
    } else {
        console.error("Error: Elemento con ID 'filter-value-despacho' no encontrado para Despacho. Revisa tu Despacho.html");
    }

    fetchDespachoData();
});