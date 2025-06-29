// === CONFIGURACIÓN PARA STOCK: Cambia esta variable para alternar la fuente de datos ===
const USE_MOCK_DATA_STOCK = false; // true: para usar mock, false: para usar API externa

// URLs de las APIs para Stock
const STOCK_MOCK_DATA_URL = '/static/js/stock_datos_mock.json'; // Tu JSON mock local
const STOCK_EXTERNAL_API_URL = '/api/proxy/stock/';

// === Selectores para la TABLA DE STOCK ===
const stockTableBody = document.getElementById('stock-table');
const filterColumnSelectStock = document.getElementById('filter-column-stock');
const filterValueInputStock = document.getElementById('filter-value-stock');
const applyFilterButtonStock = document.getElementById('apply-filter-stock');
const sortColumnSelectStock = document.getElementById('sort-column-stock');
const sortOrderSelectStock = document.getElementById('sort-order-stock');
const applySortButtonStock = document.getElementById('apply-sort-stock');

let allStockData = []; // Guarda todos los datos originales de stock

// === FUNCIONES DE CARGA Y RENDERIZADO DE DATOS PARA STOCK ===
async function fetchAndRenderStock() {
    if (!stockTableBody) {
        console.error('Error: Elemento #stock-table no encontrado en Stock.html.');
        return;
    }
    stockTableBody.innerHTML = ''; // Limpiar tabla antes de añadir nuevos datos

    let urlToFetch = '';
    let errorMessage = '';

    if (USE_MOCK_DATA_STOCK) {
        urlToFetch = STOCK_MOCK_DATA_URL;
        errorMessage = 'Error al obtener los datos de stock desde stock_datos_mock.json:';
    } else {
        urlToFetch = STOCK_EXTERNAL_API_URL;
        errorMessage = `Error al obtener los datos de stock desde ${STOCK_EXTERNAL_API_URL}:`;
    }

    try {
        const response = await fetch(urlToFetch);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        // **AQUÍ ESTÁ EL CAMBIO CLAVE: Mapeo de datos para la API de Azure**
        allStockData = data.map(item => ({
            id: item.id || 'N/A',
            // Usamos 'name' de la API para 'title' en la tabla
            title: item.name || 'N/A',
            // La API tiene 'categoryId'. Si tienes un mapeo de categoryId a nombre de categoría,
            // lo pondrías aquí. Por ahora, mostraremos el categoryId directamente.
            category: item.categoryId || 'N/A', // Mapeamos categoryId a 'category'
            price: item.price || 'N/A'
        }));

        renderStockTable(allStockData);

    } catch (error) {
        console.error(errorMessage, error);
        stockTableBody.innerHTML = `<tr><td colspan="4">${errorMessage.replace(':', '')}</td></tr>`; // 4 columnas
    }
}

function renderStockTable(stockEntries) {
    if (!stockTableBody) return;
    stockTableBody.innerHTML = ''; // Limpiar la tabla

    stockEntries.forEach(item => {
        const row = stockTableBody.insertRow();
        row.insertCell().textContent = item.id;
        row.insertCell().textContent = item.title;
        row.insertCell().textContent = item.category; // Ahora mostrará el categoryId
        row.insertCell().textContent = item.price;
    });
}

// Las funciones applyStockFilter y applyStockSort también necesitan ser ajustadas
// para usar 'title' en lugar de 'name' si es que las usabas así antes.
// Ya las había ajustado en el código anterior, pero lo confirmo.

function applyStockFilter() {
    if (!filterColumnSelectStock || !filterValueInputStock) return;

    const column = filterColumnSelectStock.value;
    const value = filterValueInputStock.value.toLowerCase();

    const filteredEntries = allStockData.filter(item => {
        let cellValue = '';
        if (column === 'title') { // Filtrar por 'title' que es el 'name' de la API
            cellValue = String(item.title || '').toLowerCase();
        } else if (column === 'category') { // Filtrar por 'category' que es el 'categoryId' de la API
            cellValue = String(item.category || '').toLowerCase();
        }
        // Puedes añadir más condiciones de filtro si deseas filtrar por SKU, description, etc.
        return cellValue.includes(value);
    });
    renderStockTable(filteredEntries);
}

function applyStockSort() {
    if (!sortColumnSelectStock || !sortOrderSelectStock) return;

    const column = sortColumnSelectStock.value;
    const order = sortOrderSelectStock.value;

    const sortedEntries = [...allStockData].sort((a, b) => {
        let valueA = a[column];
        let valueB = b[column];

        if (column === 'id' || column === 'price' || column === 'category') { // 'category' (categoryId) también es numérico
            valueA = parseFloat(valueA);
            valueB = parseFloat(valueB);
            if (isNaN(valueA)) valueA = (order === 'asc' ? Number.MIN_SAFE_INTEGER : Number.MAX_SAFE_INTEGER);
            if (isNaN(valueB)) valueB = (order === 'asc' ? Number.MIN_SAFE_INTEGER : Number.MAX_SAFE_INTEGER);

            if (order === 'asc') {
                return valueA - valueB;
            } else {
                return valueB - valueA;
            }
        } else { // Para valores de texto (title)
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
    renderStockTable(sortedEntries);
}

// === EVENT LISTENERS y LÓGICA DE INICIO para STOCK ===
document.addEventListener('DOMContentLoaded', () => {
    fetchAndRenderStock();

    if (applyFilterButtonStock) {
        applyFilterButtonStock.addEventListener('click', applyStockFilter);
    }
    if (applySortButtonStock) {
        applySortButtonStock.addEventListener('click', applyStockSort);
    }
});