document.addEventListener('DOMContentLoaded', function() {
    function updateCurrentDate() {
        const dateElement = document.getElementById('current-date');
        if (dateElement) {
            const today = new Date();
            const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
            const formattedDate = today.toLocaleDateString('es-CL', options); // 'es-CL' para formato DD/MM/YYYY
            dateElement.textContent = formattedDate;
        }
    }
    // Llama a la función para establecer la fecha cuando la página cargue
    updateCurrentDate();
});