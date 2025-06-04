const filterColumnSelect = document.getElementById('filter-column');
const filterValueInput = document.getElementById('filter-value');
const applyFilterButton = document.getElementById('apply-filter');
const productsTableBody = document.getElementById('products-table');
const applySortButton = document.getElementById('apply-sort');
const sortColumnSelect = document.getElementById('sort-column');
const sortOrderSelect = document.getElementById('sort-order');

let allProductsData = [];

async function loadProductsData() {
    try {
        const response = await fetch('https://fakestoreapi.com/products');
        const data = await response.json();
        allProductsData = data;
        renderProductsTable(data);
    } catch (error) {
        console.error('Error al obtener los productos:', error);
    }
}

function renderProductsTable(products) {
    productsTableBody.innerHTML = '';
    products.forEach(product => {
        const row = productsTableBody.insertRow();
        const idProduct = row.insertCell();
        const titleProduct = row.insertCell();
        const categoryProduct = row.insertCell();
        const priceProduct = row.insertCell();

        idProduct.textContent = product.id;
        titleProduct.textContent = product.title;
        categoryProduct.textContent = product.category;
        priceProduct.textContent = product.price;        
    });
}

function applyFilter() {
    const column = filterColumnSelect.value;
    const value = filterValueInput.value.toLowerCase();
    const filtered = allProductsData.filter(product =>
        String(product[column]).toLowerCase().includes(value)
    );
    renderProductsTable(filtered);
}

function applySort() {
    const column = sortColumnSelect.value;
    const order = sortOrderSelect.value;

    const sorted = [...allProductsData].sort((a, b) => {
        let valA = a[column];
        let valB = b[column];

        if (typeof valA === 'string') valA = valA.toLowerCase();
        if (typeof valB === 'string') valB = valB.toLowerCase();

        if (valA < valB) return order === 'asc' ? -1 : 1;
        if (valA > valB) return order === 'asc' ? 1 : -1;
        return 0;
    });

    renderProductsTable(sorted);
}

// Eventos
applyFilterButton.addEventListener('click', applyFilter);
applySortButton.addEventListener('click', applySort);
window.addEventListener('load', loadProductsData);
