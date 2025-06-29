document.addEventListener('DOMContentLoaded', function() {
    // Definiciones de elementos del DOM
    // ¡VERIFICA ESTOS IDS CONTRA TU HTML!
    const tableBody = document.getElementById('proveedores-table');
    const filterColumnSelect = document.getElementById('filter-column-prov');
    const filterValueInput = document.getElementById('filter-value-prov');
    const applyFilterButton = document.getElementById('apply-filter-prov');
    const sortColumnSelect = document.getElementById('sort-column-prov');
    const sortOrderSelect = document.getElementById('sort-order-prov');
    const applySortButton = document.getElementById('apply-sort-prov');

    let allProveedoresData = [];

    async function fetchProveedoresData() {
        try {
           
            const response = await fetch('/static/js/Provee_datos_mock.json');
            
            if (!response.ok) {
                // Lanzar un error más específico para depuración
                throw new Error(`HTTP error! status: ${response.status} (${response.statusText}) - Asegúrate que 'proveedores_datos_mock.json' está en main_api/static/js/`);
            }
            allProveedoresData = await response.json();
            renderTable(allProveedoresData);
        } catch (error) {
            console.error('Error fetching proveedores data:', error);
            // Mostrar un mensaje de error en la tabla si no se cargan los datos
            if (tableBody) { // Solo si tableBody se encontró
                tableBody.innerHTML = '<tr><td colspan="4">Error al cargar los datos de proveedores. Verifica la consola para más detalles y la existencia de proveedores_datos_mock.json.</td></tr>';
            }
        }
    }

    function renderTable(data) {
        if (!tableBody) { // Verificar si tableBody es null antes de usarlo
            console.error("Error: Elemento 'proveedores-table' no encontrado para renderizar.");
            return;
        }
        tableBody.innerHTML = '';
        if (data.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="4">No hay proveedores para mostrar.</td></tr>';
            return;
        }
        data.forEach(proveedor => {
            const row = tableBody.insertRow();
            row.insertCell().textContent = proveedor.id;
            row.insertCell().textContent = proveedor.nombre;
            row.insertCell().textContent = proveedor.contacto;
            row.insertCell().textContent = proveedor.telefono;
        });
    }

    function applyFiltersAndSort() {
        let filteredData = [...allProveedoresData];
        
        // Solo proceder si los elementos existen
        if (filterColumnSelect && filterValueInput) {
            const filterColumn = filterColumnSelect.value;
            const filterValue = filterValueInput.value.toLowerCase();

            if (filterValue) {
                filteredData = filteredData.filter(item => {
                    let itemValue;
                    if (filterColumn === 'nombre') { 
                        itemValue = item.nombre;
                    } else if (filterColumn === 'contacto') {
                        itemValue = item.contacto;
                    } else if (filterColumn === 'categoria') { 
                        itemValue = item.categoria;
                    }
                    return itemValue && itemValue.toString().toLowerCase().includes(filterValue);
                });
            }
        } else {
            console.warn("Elementos de filtro no encontrados, omitiendo filtrado.");
        }

        // Solo proceder si los elementos existen
        if (sortColumnSelect && sortOrderSelect) {
            const sortColumn = sortColumnSelect.value;
            const sortOrder = sortOrderSelect.value;

            filteredData.sort((a, b) => {
                let valA, valB;
                if (sortColumn === 'id') {
                    valA = a.id;
                    valB = b.id;
                } else if (sortColumn === 'nombre') { 
                    valA = a.nombre;
                    valB = b.nombre;
                } else if (sortColumn === 'telefono') { 
                    valA = a.telefono; 
                    valB = b.telefono; 
                }
                
                if (typeof valA === 'number' && typeof valB === 'number') {
                    return sortOrder === 'asc' ? valA - valB : valB - valA;
                } else { 
                    const comparison = String(valA || '').localeCompare(String(valB || ''));
                    return sortOrder === 'asc' ? comparison : -comparison;
                }
            });
        } else {
            console.warn("Elementos de ordenamiento no encontrados, omitiendo ordenamiento.");
        }

        renderTable(filteredData);
    }

    // AÑADIMOS CHEQUEOS DE NULIDAD ANTES DE AÑADIR EVENT LISTENERS
    // La línea 102 en tu Provee.js es donde se añade el addEventListener
    // ¡Esto es lo que debemos depurar con mucho cuidado!
    if (applyFilterButton) { // Si applyFilterButton es null, este bloque no se ejecuta
        applyFilterButton.addEventListener('click', applyFiltersAndSort);
    } else {
        console.error("Error: Elemento con ID 'apply-filter-prov' no encontrado en el DOM. Revisa tu Proveedores.html");
    }

    if (applySortButton) { // Si applySortButton es null, este bloque no se ejecuta
        applySortButton.addEventListener('click', applyFiltersAndSort);
    } else {
        console.error("Error: Elemento con ID 'apply-sort-prov' no encontrado en el DOM. Revisa tu Proveedores.html");
    }

    if (filterValueInput) { // Si filterValueInput es null, este bloque no se ejecuta
        filterValueInput.addEventListener('keyup', (event) => {
            if (event.key === 'Enter') {
                applyFiltersAndSort();
            }
        });
    } else {
        console.error("Error: Elemento con ID 'filter-value-prov' no encontrado en el DOM. Revisa tu Proveedores.html");
    }

    fetchProveedoresData();
});