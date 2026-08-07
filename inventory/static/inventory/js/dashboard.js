document.addEventListener('DOMContentLoaded', function () {
    Chart.defaults.font.family = 'Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
    Chart.defaults.color = '#495057';

    const salesCanvas = document.getElementById('salesChart');
    if (salesCanvas) {
        const salesCtx = salesCanvas.getContext('2d');
        const salesData = JSON.parse(salesCanvas.dataset.values || '[]');
        const salesHeight = salesCanvas.clientHeight || salesCanvas.height || 320;
        const salesGradient = salesCtx.createLinearGradient(0, 0, 0, salesHeight);
        salesGradient.addColorStop(0, 'rgba(13, 110, 253, 0.24)');
        salesGradient.addColorStop(1, 'rgba(13, 110, 253, 0.03)');

        new Chart(salesCanvas, {
            type: 'line',
            data: {
                labels: JSON.parse(salesCanvas.dataset.labels || '[]'),
                datasets: [
                    {
                        label: 'Sales',
                        data: salesData,
                        backgroundColor: salesGradient,
                        borderColor: 'rgba(13, 110, 253, 0.95)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.38,
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        pointBackgroundColor: 'rgba(13, 110, 253, 1)',
                        pointBorderColor: '#ffffff',
                        pointBorderWidth: 2,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 800,
                },
                interaction: {
                    mode: 'nearest',
                    intersect: false,
                },
                plugins: {
                    legend: {
                        display: false,
                    },
                    tooltip: {
                        backgroundColor: '#ffffff',
                        borderColor: 'rgba(15, 23, 42, 0.08)',
                        borderWidth: 1,
                        titleColor: '#212529',
                        bodyColor: '#212529',
                        displayColors: false,
                        callbacks: {
                            label: function (context) {
                                return '₹ ' + context.formattedValue;
                            },
                        },
                    },
                },
                scales: {
                    x: {
                        grid: {
                            display: false,
                        },
                        ticks: {
                            color: '#6c757d',
                            maxRotation: 45,
                            minRotation: 0,
                            autoSkip: true,
                            autoSkipPadding: 12,
                        },
                        border: {
                            color: 'rgba(226, 232, 240, 0.9)',
                        },
                    },
                    y: {
                        grid: {
                            color: 'rgba(226, 232, 240, 0.85)',
                            drawBorder: false,
                        },
                        ticks: {
                            color: '#6c757d',
                            callback: function (value) {
                                return '₹ ' + value;
                            },
                        },
                    },
                },
            },
        });
    }

    const stockCanvas = document.getElementById('stockChart');
    if (stockCanvas) {
        const stockCtx = stockCanvas.getContext('2d');
        const stockHeight = stockCanvas.clientHeight || stockCanvas.height || 320;
        const productGradient = stockCtx.createLinearGradient(0, 0, 0, stockHeight);
        productGradient.addColorStop(0, 'rgba(25, 135, 84, 0.9)');
        productGradient.addColorStop(1, 'rgba(25, 135, 84, 0.35)');

        new Chart(stockCanvas, {
            type: 'bar',
            data: {
                labels: JSON.parse(stockCanvas.dataset.labels || '[]'),
                datasets: [
                    {
                        label: 'Stock Qty',
                        data: JSON.parse(stockCanvas.dataset.values || '[]'),
                        backgroundColor: productGradient,
                        borderRadius: 12,
                        maxBarThickness: 36,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 700,
                },
                plugins: {
                    legend: {
                        display: false,
                    },
                    tooltip: {
                        backgroundColor: '#ffffff',
                        borderColor: 'rgba(15, 23, 42, 0.08)',
                        borderWidth: 1,
                        titleColor: '#212529',
                        bodyColor: '#212529',
                        displayColors: false,
                        callbacks: {
                            label: function (context) {
                                return context.dataset.label + ': ' + context.formattedValue;
                            },
                        },
                    },
                },
                scales: {
                    x: {
                        grid: {
                            display: false,
                        },
                        ticks: {
                            color: '#6c757d',
                            autoSkip: false,
                            maxRotation: 45,
                            minRotation: 0,
                        },
                        border: {
                            color: 'rgba(226, 232, 240, 0.9)',
                        },
                    },
                    y: {
                        grid: {
                            color: 'rgba(226, 232, 240, 0.85)',
                        },
                        ticks: {
                            color: '#6c757d',
                            beginAtZero: true,
                            precision: 0,
                        },
                    },
                },
            },
        });
    }
});
