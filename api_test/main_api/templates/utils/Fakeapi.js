const filterColumnSelect = document.getElementById('filter-column');
const filterValueInput = document.getElementById('filter-value');
const applyFilterButton = document.getElementById('apply-filter');
const securityUsersTableBody = document.getElementById('security-users');
let allUsersData = []; // Guarda todos los datos originales

async function loadSecurityUsersData() {
    try {
        const response = await fetch('https://jsonplaceholder.typicode.com/users');
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
        const usernameCell = row.insertCell();
        const nameCell = row.insertCell();
        const emailCell = row.insertCell();

        idCell.textContent = user.id;
        usernameCell.textContent = user.username;
        nameCell.textContent = user.name;
        emailCell.textContent = user.email;
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

// Aquí podrías tener lógica para el ordenamiento si la implementas.
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