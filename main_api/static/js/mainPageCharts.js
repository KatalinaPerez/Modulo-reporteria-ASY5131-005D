document.addEventListener('DOMContentLoaded', function() {

    // Función genérica para cargar datos de una API y actualizar el HTML y dibujar gráficos
    async function loadDataAndPopulate(api_url, selectors, chartConfigFn = null) {
        try {
            const response = await fetch(api_url);
            if (!response.ok) {
                throw new Error(`Error HTTP! status: ${response.status}`);
            }
            const data = await response.json();

            // Monetization
            if (selectors.monetization) {
                document.querySelector(selectors.monetization.value).textContent = `$${data.totalRevenue.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
                document.querySelector(selectors.monetization.change).textContent = `+${data.revenueChangePercent}%`;
                
                const topProductsBody = document.querySelector(selectors.monetization.tableBody);
                if (topProductsBody) {
                    topProductsBody.innerHTML = '';
                    data.topProducts.forEach(item => {
                        const row = document.createElement('tr');
                        row.innerHTML = `<td>${item.product}</td><td class="right">$${item.revenue.toLocaleString('en-US', {minimumFractionDigits: 1, maximumFractionDigits: 1})}</td>`;
                        topProductsBody.appendChild(row);
                    });
                    if (data.totalRevenue && !topProductsBody.querySelector('.grand-total-row')) {
                        const totalRow = document.createElement('tr');
                        totalRow.className = 'grand-total-row';
                        totalRow.innerHTML = `<td>Grand total</td><td class="right">$${data.totalRevenue.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>`;
                        topProductsBody.appendChild(totalRow);
                    }
                }
                // DIBUJAR GRÁFICO DE MONETIZACIÓN
                if (chartConfigFn && selectors.monetization.chartCanvasId) {
                    chartConfigFn(selectors.monetization.chartCanvasId, data.chartData, 'line');
                }
            }

            // Engagement
            if (selectors.engagement) {
                document.querySelector(selectors.engagement.value).textContent = data.totalViews.toLocaleString('en-US');
                document.querySelector(selectors.engagement.change).textContent = `+${data.viewChangePercent}%`;
                
                const topPagesBody = document.querySelector(selectors.engagement.tableBody);
                if (topPagesBody) {
                    topPagesBody.innerHTML = '';
                    data.topPages.forEach(item => {
                        const row = document.createElement('tr');
                        row.innerHTML = `<td>${item.title}</td><td class="right">${item.views.toLocaleString('en-US')}</td>`;
                        topPagesBody.appendChild(row);
                    });
                }
                // DIBUJAR GRÁFICO DE ENGAGEMENT
                if (chartConfigFn && selectors.engagement.chartCanvasId) {
                    chartConfigFn(selectors.engagement.chartCanvasId, data.chartData, 'line');
                }
            }

            // Acquisition
            if (selectors.acquisition) {
                document.querySelector(selectors.acquisition.value).textContent = data.totalUsers.toLocaleString('en-US');
                document.querySelector(selectors.acquisition.change).textContent = `+${data.userChangePercent}%`;

                const topSourcesBody = document.querySelector(selectors.acquisition.tableBody);
                if (topSourcesBody) {
                    topSourcesBody.innerHTML = '';
                    data.topSources.forEach(item => {
                        const row = document.createElement('tr');
                        row.innerHTML = `<td>${item.source}</td><td class="right">${item.users.toLocaleString('en-US')}</td>`;
                        topSourcesBody.appendChild(row);
                    });
                }
                // DIBUJAR GRÁFICO DE ACQUISITION (ej. de barras)
                if (chartConfigFn && selectors.acquisition.chartCanvasId) {
                    chartConfigFn(selectors.acquisition.chartCanvasId, data.chartData, 'bar', 'month', 'users');
                }
            }

            // Audience
            if (selectors.audience) {
                if (selectors.audience.geoValue) {
                    document.querySelector(selectors.audience.geoValue).textContent = data.geoChartValue.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
                }
                // DIBUJAR GRÁFICOS DE AUDIENCE (ej. de pastel para demografía y tecnología)
                if (chartConfigFn && selectors.audience.demographicsChartCanvasId) {
                    chartConfigFn(selectors.audience.demographicsChartCanvasId, data.demographics, 'pie', 'age_group', 'users');
                }
                if (chartConfigFn && selectors.audience.techChartCanvasId) {
                    chartConfigFn(selectors.audience.techChartCanvasId, data.tech, 'pie', 'device', 'users');
                }
                // Para el mapa geo, Chart.js no es lo ideal. Podrías dejar la imagen o usar Google Charts/Leaflet.
                // Si quieres un placeholder de canvas, podemos ponerlo para mantener la estructura:
                if (chartConfigFn && selectors.audience.geoChartCanvasId) {
                    // Aquí podrías intentar dibujar algo simple o dejarlo como un placeholder si no usarás Chart.js para mapas
                    console.log('Geo chart data loaded, consider a specific library for maps.');
                }
            }

        } catch (error) {
            console.error(`Error loading data from ${api_url}:`, error);
            // Opcional: mostrar un mensaje de error en la UI
        }
    }

    // --- Funciones para dibujar gráficos con Chart.js ---
    let myCharts = {}; // Objeto para guardar instancias de gráficos y poder destruirlas/actualizarlas

    function renderChart(canvasId, chartData, type, labelKey = null, dataKey = null) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) {
            console.error(`Canvas con ID '${canvasId}' no encontrado.`);
            return;
        }

        // Destruir gráfico existente si ya lo hay
        if (myCharts[canvasId]) {
            myCharts[canvasId].destroy();
        }

        let labels, dataValues;

        if (type === 'line' || type === 'bar') {
            labels = chartData.map(d => d.date || d[labelKey]); // Usa 'date' por defecto, o el 'labelKey'
            dataValues = chartData.map(d => d.revenue || d.views || d[dataKey]); // Usa 'revenue'/'views' por defecto, o el 'dataKey'
        } else if (type === 'pie' || type === 'doughnut') {
            labels = chartData.map(d => d[labelKey]);
            dataValues = chartData.map(d => d[dataKey]);
        }

        const backgroundColors = [
            'rgba(255, 99, 132, 0.6)',
            'rgba(54, 162, 235, 0.6)',
            'rgba(255, 206, 86, 0.6)',
            'rgba(75, 192, 192, 0.6)',
            'rgba(153, 102, 255, 0.6)',
            'rgba(255, 159, 64, 0.6)'
        ];
        const borderColors = [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
        ];

        let dataset = {
            label: 'Valor', // Título genérico del dataset
            data: dataValues,
            backgroundColor: backgroundColors.slice(0, labels.length), // Asegura que haya suficientes colores
            borderColor: borderColors.slice(0, labels.length),
            borderWidth: 1
        };

        if (type === 'line') {
            dataset.fill = false; // Solo la línea, no el área bajo la línea
        }

        myCharts[canvasId] = new Chart(ctx, {
            type: type,
            data: {
                labels: labels,
                datasets: [dataset]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false, // Permite que el gráfico se ajuste al tamaño del contenedor div.chart
                plugins: {
                    legend: {
                        display: true, // Muestra la leyenda
                        position: 'top',
                    },
                    title: {
                        display: false, // No mostrar título dentro del gráfico, ya lo tienes en el H3
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        display: (type !== 'pie' && type !== 'doughnut') // Ocultar ejes Y para gráficos de pastel
                    },
                    x: {
                        display: (type !== 'pie' && type !== 'doughnut') // Ocultar ejes X para gráficos de pastel
                    }
                }
            }
        });
    }

    // --- NUEVAS FUNCIONES PARA CARGAR CONTADORES ---

    async function loadCounter(api_url, element_id, label) {
        try {
            const response = await fetch(api_url);
            if (!response.ok) {
                throw new Error(`Error HTTP! status: ${response.status}`);
            }
            const data = await response.json();
            
            const countElement = document.getElementById(element_id);
            if (countElement) {
                // Asumiendo que la API devuelve { 'stockCount': N } o { 'securityUsersCount': N }
                const value = data.stockCount !== undefined ? data.stockCount : data.securityUsersCount;
                countElement.textContent = value.toLocaleString('en-US'); // Formato numérico
            } else {
                console.warn(`Elemento con ID '${element_id}' no encontrado para el contador.`);
            }
        } catch (error) {
            console.error(`Error al cargar el contador de ${label}:`, error);
            const countElement = document.getElementById(element_id);
            if (countElement) {
                countElement.textContent = 'Error';
            }
        }
    }

    // --- LLAMADAS A LAS FUNCIONES DE CARGA ---

    // Llamadas para los contadores (deben ir al inicio del DOMContentLoaded)
    loadCounter('/api/stock-count/', 'stock-count', 'stock');
    loadCounter('/api/security-users-count/', 'security-users-count', 'usuarios de seguridad');

    // Llamadas para las secciones de gráficos (existentes)
    loadDataAndPopulate('/api/monetization-data/', {
        monetization: {
            value: '.monetization .metric-value',
            change: '.monetization .metric-change',
            tableBody: '.monetization .table-summary tbody',
            chartCanvasId: 'monetizationChartCanvas' // ID del canvas para este gráfico
        }
    }, renderChart);

    loadDataAndPopulate('/api/engagement-data/', {
        engagement: {
            value: '.engagement .metric-value',
            change: '.engagement .metric-change',
            tableBody: '.engagement .table-summary tbody',
            chartCanvasId: 'engagementChartCanvas'
        }
    }, renderChart);

    loadDataAndPopulate('/api/acquisition-data/', {
        acquisition: {
            value: '.acquisition .metric-value',
            change: '.acquisition .metric-change',
            tableBody: '.acquisition .table-summary tbody',
            chartCanvasId: 'acquisitionChartCanvas'
        }
    }, renderChart);

    loadDataAndPopulate('/api/audience-data/', {
        audience: {
            geoValue: '.audience .geo-chart .value',
            demographicsChartCanvasId: 'demographicsChartCanvas',
            techChartCanvasId: 'techChartCanvas',
            geoChartCanvasId: 'geoChartCanvas' // Aunque Chart.js no haga mapas, mantenemos la estructura
        }
    }, renderChart);
});