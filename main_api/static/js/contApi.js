// === CONFIGURACIÓN: Cambia esta variable para alternar la fuente de datos ===
// true: Usará cont_datos_mock.json (tu archivo local)
// false: Usará una API externa (JSONPlaceholder como ejemplo, o tu API real cuando la tengas)
const USE_MOCK_DATA_CONT = true ; // <--- CÁMBIAME para alternar!

// URLs de las APIs
const CONTABILIDAD_MOCK_DATA_URL = '/static/js/cont_datos_mock.json'; // Tu JSON mock local
const JSONPLACEHOLDER_CONTABILIDAD_API_URL = 'https://jsonplaceholder.typicode.com/posts?_limit=15'; // Para simular entradas de contabilidad

// === Selectores para la TABLA DE CONTABILIDAD ===
const contabilidadTableBody = document.getElementById('contabilidad-table');
const filterColumnSelectCont = document.getElementById('filter-column-cont');
const filterValueInputCont = document.getElementById('filter-value-cont');
const applyFilterButtonCont = document.getElementById('apply-filter-cont');
const sortColumnSelectCont = document.getElementById('sort-column-cont');
const sortOrderSelectCont = document.getElementById('sort-order-cont');
const applySortButtonCont = document.getElementById('apply-sort-cont');

let allContabilidadData = []; // Guarda todos los datos originales de contabilidad

// === FUNCIONES DE CARGA Y RENDERIZADO DE DATOS PARA CONTABILIDAD ===
async function fetchAndRenderContabilidad() {
    if (!contabilidadTableBody) {
        console.error('Error: Elemento #contabilidad-table no encontrado en Contabilidad.html.');
        return;
    }
    contabilidadTableBody.innerHTML = ''; // Limpiar tabla antes de añadir nuevos datos

    let urlToFetch = '';
    let errorMessage = '';

    if (USE_MOCK_DATA_CONT) {
        urlToFetch = CONTABILIDAD_MOCK_DATA_URL;
        errorMessage = 'Error al obtener los datos de contabilidad desde cont_datos_mock.json:';
    } else {
        urlToFetch = JSONPLACEHOLDER_CONTABILIDAD_API_URL;
        errorMessage = 'Error al obtener los datos de contabilidad desde JSONPlaceholder:';
    }

    try {
        const response = await fetch(urlToFetch);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        // Lógica de mapeo condicional:
        if (USE_MOCK_DATA_CONT) {
            // Mapeamos los campos de tu mock a los nombres que renderContabilidadTable espera
            allContabilidadData = data.map(item => ({
                id: item.idAsiento, // Mapea idAsiento a id
                fecha: item.fechaAsiento, // Mapea fechaAsiento a fecha
                descripcion: item.descripcionAsiento, // Mapea descripcionAsiento a descripcion
                // AQUI ESTÁ EL CAMBIO CLAVE: Usa los valores directamente del item, o 'N/A' si no existen
                monto: item.monto !== undefined ? item.monto : 'N/A',
                tipo: item.tipo !== undefined ? item.tipo : 'N/A',
                referencia: item.referenciasAsiento // Añadimos la referencia
            }));
        } else {
            // Si usamos JSONPlaceholder, mapeamos sus 'posts' a nuestra estructura de 'contabilidad'.
            allContabilidadData = data.map(item => ({
                id: item.id,
                fecha: new Date(Date.now() - Math.random() * 86400000 * 30 * 12).toISOString(),
                descripcion: item.title,
                monto: (Math.random() * 1000000 + 10000).toFixed(2),
                tipo: Math.random() > 0.5 ? 'Ingreso' : 'Egreso',
                referencia: `Post ID: ${item.id}` // Para JSONPlaceholder, usamos el ID como referencia
            }));
        }

        renderContabilidadTable(allContabilidadData);

    } catch (error) {
        console.error(errorMessage, error);
        // Ajusta colspan a 5 porque ahora esperamos 5 columnas en el HTML
        contabilidadTableBody.innerHTML = `<tr><td colspan="5">${errorMessage.replace(':', '')}</td></tr>`;
    }
}

function renderContabilidadTable(contabilidadEntries) {
    if (!contabilidadTableBody) return;
    contabilidadTableBody.innerHTML = '';
    contabilidadEntries.forEach(entry => {
        const row = contabilidadTableBody.insertRow();
        row.insertCell().textContent = entry.id;
        const dateObj = new Date(entry.fecha);
        row.insertCell().textContent = dateObj.toLocaleDateString('es-ES');
        row.insertCell().textContent = entry.descripcion;
        row.insertCell().textContent = entry.monto; // Este ahora debería tener el valor numérico
        row.insertCell().textContent = entry.tipo;  // Este ahora debería tener el valor 'Ingreso'/'Egreso'
        // Si quieres mostrar la referencia, necesitarías una columna adicional en el HTML
        // row.insertCell().textContent = entry.referencia;
    });
}

function applyContabilidadFilter() {
    if (!filterColumnSelectCont || !filterValueInputCont || !contabilidadTableBody) return;

    const column = filterColumnSelectCont.value;
    const value = filterValueInputCont.value.toLowerCase();

    const filteredEntries = allContabilidadData.filter(entry => {
        let cellValue = '';
        if (column === 'descripcion') {
            cellValue = String(entry.descripcion || '').toLowerCase();
        } else if (column === 'tipo') {
            cellValue = String(entry.tipo || '').toLowerCase();
        } else if (column === 'id') {
            cellValue = String(entry.id || '').toLowerCase();
        } else if (column === 'referencia') {
            cellValue = String(entry.referencia || '').toLowerCase();
        }
        return cellValue.includes(value);
    });
    renderContabilidadTable(filteredEntries);
}

function applyContabilidadSort() {
    if (!sortColumnSelectCont || !sortOrderSelectCont || !contabilidadTableBody) return;

    const column = sortColumnSelectCont.value;
    const order = sortOrderSelectCont.value;

    const sortedEntries = [...allContabilidadData].sort((a, b) => {
        let valueA = a[column];
        let valueB = b[column];

        if (column === 'id' || column === 'monto') {
            valueA = parseFloat(valueA);
            valueB = parseFloat(valueB);
            if (isNaN(valueA)) valueA = (order === 'asc' ? Number.MIN_SAFE_INTEGER : Number.MAX_SAFE_INTEGER);
            if (isNaN(valueB)) valueB = (order === 'asc' ? Number.MIN_SAFE_INTEGER : Number.MAX_SAFE_INTEGER);

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
    renderContabilidadTable(sortedEntries);
}

// === EVENT LISTENERS y LÓGICA DE INICIO para CONTABILIDAD ===
document.addEventListener('DOMContentLoaded', () => {
    fetchAndRenderContabilidad();

    if (applyFilterButtonCont) {
        applyFilterButtonCont.addEventListener('click', applyContabilidadFilter);
    }
    if (applySortButtonCont) {
        applySortButtonCont.addEventListener('click', applyContabilidadSort);
    }

    const currentDateElement = document.getElementById('current-date');
    if (currentDateElement) {
        const today = new Date();
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        currentDateElement.textContent = today.toLocaleDateString('es-ES', options);
    }
});