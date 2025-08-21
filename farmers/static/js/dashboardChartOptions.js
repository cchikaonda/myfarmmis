document.addEventListener("DOMContentLoaded", function() {

    // Shared chart options
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false
    };

    // Initialize charts with dynamic or static data
    const charts = [
        {
            id: 'farmerChart',
            type: 'bar',
            data: {
                labels: ['Farmers'],
                datasets: [{
                    label: 'Total Farmers',
                    data: [window.farmer_count || 0],
                    backgroundColor: 'rgba(40, 167, 69, 0.6)',
                    borderColor: 'rgba(40, 167, 69, 1)',
                    borderWidth: 1
                }]
            }
        },
        {
            id: 'productionChart',
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr'],
                datasets: [{
                    label: 'Production',
                    data: [5, 8, 6, 10],
                    backgroundColor: 'rgba(0, 123, 255, 0.3)',
                    borderColor: 'rgba(0, 123, 255, 1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            }
        },
        {
            id: 'paymentsChart',
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr'],
                datasets: [{
                    label: 'Payments',
                    data: [10, 15, 12, 20],
                    backgroundColor: 'rgba(220, 53, 69, 0.2)',
                    borderColor: 'rgba(220, 53, 69, 1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            }
        },
        {
            id: 'inputDistributionChart',
            type: 'pie',
            data: {
                labels: ['Fertilizer', 'Seeds', 'Pesticides'],
                datasets: [{
                    label: 'Inputs Distribution',
                    data: [5, 3, 2],
                    backgroundColor: [
                        'rgba(0, 123, 255, 0.6)',
                        'rgba(40, 167, 69, 0.6)',
                        'rgba(255, 193, 7, 0.6)'
                    ]
                }]
            }
        },
        {
            id: 'rationChart',
            type: 'doughnut',
            data: {
                labels: ['Maize', 'Soy', 'Fishmeal', 'Minerals'],
                datasets: [{
                    label: 'Ration Formulation',
                    data: [50, 20, 20, 10],
                    backgroundColor: [
                        'rgba(255, 193, 7, 0.6)',
                        'rgba(40, 167, 69, 0.6)',
                        'rgba(0, 123, 255, 0.6)',
                        'rgba(220, 53, 69, 0.6)'
                    ]
                }]
            }
        }
    ];

    // Create all charts
    charts.forEach(cfg => {
        const ctx = document.getElementById(cfg.id);
        if (ctx) new Chart(ctx, { type: cfg.type, data: cfg.data, options: chartOptions });
    });

    // Pagination for graph cards
    const cardsPerPage = 1;
    const cards = Array.from(document.querySelectorAll('.graph-card'));
    const pagination = document.getElementById('graphPagination');
    let currentPage = 1;
    const totalPages = Math.ceil(cards.length / cardsPerPage);

    function showPage(page) {
        currentPage = page;
        cards.forEach((card, idx) => {
            card.style.display = (idx >= (page-1)*cardsPerPage && idx < page*cardsPerPage) ? 'block' : 'none';
        });

        renderPagination();
    }

    function renderPagination() {
        pagination.innerHTML = '';
        const prevClass = currentPage === 1 ? 'disabled' : '';
        const nextClass = currentPage === totalPages ? 'disabled' : '';

        pagination.innerHTML += `<li class="page-item ${prevClass}"><a class="page-link" href="#" data-page="${currentPage-1}">Previous</a></li>`;

        for (let i = 1; i <= totalPages; i++) {
            const activeClass = i === currentPage ? 'active' : '';
            pagination.innerHTML += `<li class="page-item ${activeClass}"><a class="page-link" href="#" data-page="${i}">${i}</a></li>`;
        }

        pagination.innerHTML += `<li class="page-item ${nextClass}"><a class="page-link" href="#" data-page="${currentPage+1}">Next</a></li>`;

        pagination.querySelectorAll('a.page-link').forEach(link => {
            link.addEventListener('click', e => {
                e.preventDefault();
                const page = parseInt(link.getAttribute('data-page'));
                if (page >= 1 && page <= totalPages) showPage(page);
            });
        });
    }

    showPage(1); // initial render
});
