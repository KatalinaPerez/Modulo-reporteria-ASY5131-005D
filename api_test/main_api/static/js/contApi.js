const filterColumnSelect = document.getElementById('filter-column');
const filterValueInput = document.getElementById('filter-value');
const applyFilterButton = document.getElementById('apply-filter');
const securityUsersTableBody = document.getElementById('security-users');
let allUsersData = []; // Guarda todos los datos originales

async function loadSecurityUsersData() {
    try {
        const response = await fetch('http://34.225.192.85:8000/api/schema/swagger-ui/#/');
        const usersData = await response.json();
        allUsersData = usersData; // Guarda los datos originales
        renderTable(usersData); // Renderiza la tabla inicial
    } catch (error) {
        console.error('Error al obtener los datos de usuarios:', error);
    }
}

function renderTable(users) {
    securityUsersTableBody.innerHTML = '';
    users.forEach(user => {
        const row = securityUsersTableBody.insertRow();
        const idCell = row.insertCell();
        const fechaCell = row.insertCell();
        const descriptCell = row.insertCell();
        const cityCell = row.insertCell();

        pdf.cell(60, 10, "ID Asiento", 1, 0, "C")
    pdf.cell(40, 10, "Fecha", 1, 0, "C")
    pdf.cell(40, 10, "Descripción", 1, 0, "C")
    pdf.cell(40, 10, "Referencia", 1, 1, "C")


        nameCell.textContent = user.name;
        emailCell.textContent = user.email;
        adressCell.textContent = user.address.street + ', ' + user.address.suite;
        cityCell.textContent = user.address.city;
    });
}

function applyFilter() {
    const column = filterColumnSelect.value;
    const value = filterValueInput.value.toLowerCase();
    const filteredUsers = allUsersData.filter(user =>
        String(user[column]).toLowerCase().includes(value)
    );
    renderTable(filteredUsers);
}

// Event Listeners
applyFilterButton.addEventListener('click', applyFilter);

window.onload = loadSecurityUsersData;

const sortColumnSelect = document.getElementById('sort-column');
const sortOrderSelect = document.getElementById('sort-order');
const applySortButton = document.getElementById('apply-sort');

function applySort() {
    const column = sortColumnSelect.value;
    const order = sortOrderSelect.value;

    const sortedUsers = [...allUsersData].sort((a, b) => {
        const valueA = String(a[column]).toLowerCase();
        const valueB = String(b[column]).toLowerCase();

        if (valueA < valueB) {
            return order === 'asc' ? -1 : 1;
        }
        if (valueA > valueB) {
            return order === 'asc' ? 1 : -1;
        }
        return 0;
    });
    renderTable(sortedUsers);
}

applySortButton.addEventListener('click', applySort);