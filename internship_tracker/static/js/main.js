/**
 * Internship Tracker - Main JavaScript
 */

function toggleModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.toggle('active');
    }
}

function initTableSorting(tableId, currentSort, currentDir) {
    const table = document.getElementById(tableId);
    if (!table) return;

    const headers = table.querySelectorAll('th.sortable');
    headers.forEach(header => {
        header.addEventListener('click', function() {
            const sortField = this.dataset.sort;
            let dir = 'asc';
            if (sortField === currentSort && currentDir === 'asc') {
                dir = 'desc';
            }

            const url = new URL(window.location.href);
            url.searchParams.set('sort', sortField);
            url.searchParams.set('dir', dir);
            window.location.href = url.toString();
        });
    });
}

function initFormValidation(formSelector) {
    const form = document.querySelector(formSelector);
    if (!form) return;

    form.addEventListener('submit', function(e) {
        let valid = true;
        const requiredFields = form.querySelectorAll('[required]');

        requiredFields.forEach(field => {
            removeFieldError(field);
            if (!field.value.trim()) {
                showFieldError(field, 'This field is required.');
                valid = false;
            }
        });

        const emailField = form.querySelector('[type="email"]');
        if (emailField && emailField.value.trim()) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(emailField.value.trim())) {
                showFieldError(emailField, 'Invalid email format.');
                valid = false;
            }
        }

        const urlField = form.querySelector('[type="url"]');
        if (urlField && urlField.value.trim()) {
            try {
                const parsed = new URL(urlField.value.trim());
                if (!['http:', 'https:'].includes(parsed.protocol)) {
                    throw new Error('Invalid protocol');
                }
            } catch {
                showFieldError(urlField, 'Invalid URL format.');
                valid = false;
            }
        }

        if (!valid) {
            e.preventDefault();
        }
    });
}

function showFieldError(field, message) {
    field.classList.add('error');
    const error = document.createElement('div');
    error.className = 'form-error';
    error.textContent = message;
    field.parentNode.appendChild(error);
}

function removeFieldError(field) {
    field.classList.remove('error');
    const existing = field.parentNode.querySelector('.form-error');
    if (existing) {
        existing.remove();
    }
}

function initDashboardCharts(statusLabels, statusValues, monthLabels, monthValues) {
    const chartColors = [
        '#2563eb', '#16a34a', '#dc2626', '#7c3aed',
        '#f59e0b', '#0891b2', '#64748b'
    ];

    const statusCtx = document.getElementById('statusChart');
    if (statusCtx) {
        new Chart(statusCtx, {
            type: 'pie',
            data: {
                labels: statusLabels,
                datasets: [{
                    data: statusValues,
                    backgroundColor: chartColors.slice(0, statusLabels.length),
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }

    const monthCtx = document.getElementById('monthChart');
    if (monthCtx) {
        new Chart(monthCtx, {
            type: 'bar',
            data: {
                labels: monthLabels,
                datasets: [{
                    label: 'Applications',
                    data: monthValues,
                    backgroundColor: '#2563eb',
                    borderRadius: 4,
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1 }
                    }
                }
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');

    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('open');
        });

        document.addEventListener('click', function(e) {
            if (sidebar.classList.contains('open') &&
                !sidebar.contains(e.target) &&
                !menuToggle.contains(e.target)) {
                sidebar.classList.remove('open');
            }
        });
    }

    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });
    });
});
