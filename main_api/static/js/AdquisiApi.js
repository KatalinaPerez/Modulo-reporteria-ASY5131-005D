// main_api/static/js/adquisiciones.js

// === CONFIGURACIÓN: Cambia esta variable para alternar la fuente de datos ===
// true: Usará adq_datos_mock.json (tu archivo local)
// false: Usará JSONPlaceholder (API externa de prueba)
const USE_MOCK_DATA = false; // <--- CÁMBIAME para alternar!

// URL de la API externa (JSONPlaceholder para posts, que usaremos como ejemplo de adquisiciones)
const JSONPLACEHOLDER_API_URL = 'https://jsonplaceholder.typicode.com/posts?_limit=20'; 

// === Selectores para la TABLA DE ADQUISICIONES ===
const adquisicionesTableBody = document.getElementById('products-table');
const filterColumnSelect = document.getElementById('filter-column');
const filterValueInput = document.getElementById('filter-value');
const applyFilterButton = document.getElementById('apply-filter');
const sortColumnSelect = document.getElementById('sort-column');
const sortOrderSelect = document.getElementById('sort-order');
const applySortButton = document.getElementById('apply-sort');

let allAdquisicionesData = [];

// === FUNCIONES DE CARGA Y RENDERIZADO DE DATOS PARA ADQUISICIONES ===
async function fetchAndRenderAdquisiciones() {
    if (!adquisicionesTableBody) {
        console.error('Error: Elemento #products-table no encontrado en Adquisiciones.html.');
        return;
    }
    adquisicionesTableBody.innerHTML = '';

    let urlToFetch = '';
    let errorMessage = '';

    if (USE_MOCK_DATA) {
        // Usar el archivo JSON mock local
        urlToFetch = '/static/js/adq_datos_mock.json';
        errorMessage = 'Error al obtener los datos de adquisiciones desde adq_datos_mock.json:';
    } else {
        // Usar la API de JSONPlaceholder
        urlToFetch = JSONPLACEHOLDER_API_URL;
        errorMessage = 'Error al obtener los datos de adquisiciones desde JSONPlaceholder:';
    }

    try {
        const response = await fetch(urlToFetch);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        // Lógica de mapeo condicional:
        // Si estamos usando JSONPlaceholder, mapeamos sus 'posts' a nuestra estructura de 'adquisiciones'.
        // Si estamos usando el mock local, los datos ya tienen la estructura correcta.
        if (!USE_MOCK_DATA) {
            allAdquisicionesData = data.map(item => ({
                id: item.id,
                // Generamos una fecha aleatoria para simular fechas de adquisición
                fecha: new Date(Date.now() - Math.random() * 86400000 * 30 * 6).toISOString(), // Fecha en los últimos 6 meses
                // Generamos precios y cantidades aleatorias
                precio_compra: (Math.random() * 500000 + 10000).toFixed(2), // Precios entre 10,000 y 510,000
                cantidad: Math.floor(Math.random() * 5) + 1, // Cantidad entre 1 y 5
                producto: item.title // Usamos el título del post como nombre de producto
            }));
        } else {
            allAdquisicionesData = data;
        }
        
        renderAdquisicionesTable(allAdquisicionesData);

    } catch (error) {
        console.error(errorMessage, error);
        adquisicionesTableBody.innerHTML = `<tr><td colspan="5">${errorMessage.replace(':', '')}</td></tr>`;
    }
}

function renderAdquisicionesTable(adquisiciones) {
    if (!adquisicionesTableBody) return;
    adquisicionesTableBody.innerHTML = '';
    adquisiciones.forEach(adquisicion => {
        const row = adquisicionesTableBody.insertRow();
        row.insertCell().textContent = adquisicion.id;
        // La fecha de JSONPlaceholder no es real, pero la generada sí es Date object
        const dateObj = new Date(adquisicion.fecha);
        row.insertCell().textContent = dateObj.toLocaleDateString('es-ES');
        row.insertCell().textContent = `$${parseFloat(adquisicion.precio_compra).toFixed(2)}`;
        row.insertCell().textContent = adquisicion.cantidad;
        row.insertCell().textContent = adquisicion.producto;
    });
}

function applyAdquisicionesFilter() {
    if (!filterColumnSelect || !filterValueInput || !adquisicionesTableBody) return;
    const column = filterColumnSelect.value;
    const value = filterValueInput.value.toLowerCase();
    
    const filteredAdquisiciones = allAdquisicionesData.filter(adquisicion => {
        const cellValue = String(adquisicion[column] || '').toLowerCase();
        return cellValue.includes(value);
    });
    renderAdquisicionesTable(filteredAdquisiciones);
}

function applyAdquisicionesSort() {
    if (!sortColumnSelect || !sortOrderSelect || !adquisicionesTableBody) return;
    const column = sortColumnSelect.value;
    const order = sortOrderSelect.value;

    const sortedAdquisiciones = [...allAdquisicionesData].sort((a, b) => {
        let valueA = a[column];
        let valueB = b[column];

        if (column === 'id' || column === 'precio_compra' || column === 'cantidad') {
            valueA = parseFloat(valueA);
            valueB = parseFloat(valueB);
            if (order === 'asc') {
                return valueA - valueB;
            } else {
                return valueB - valueA;
            }
        } else {
            valueA = String(valueA || '').toLowerCase();
            valueB = String(valueB || '').toLowerCase();

            if (valueA < valueB) {
                return order === 'asc' ? -1 : 1;
            }
            if (valueA > valueB) {
                return order === 'asc' ? 1 : -1;
            }
        }
        return 0;
    });
    renderAdquisicionesTable(sortedAdquisiciones);
}

document.addEventListener('DOMContentLoaded', () => {
    fetchAndRenderAdquisiciones();

    if (applyFilterButton) {
        applyFilterButton.addEventListener('click', applyAdquisicionesFilter);
    }
    if (applySortButton) {
        applySortButton.addEventListener('click', applyAdquisicionesSort);
    }

    const currentDateElement = document.getElementById('current-date');
    if (currentDateElement) {
        const today = new Date();
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        currentDateElement.textContent = today.toLocaleDateString('es-ES', options);
    }
});