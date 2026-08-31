/**
 * DreamHome Studio — Reports & Analytics View Controller
 * Exportable business intelligence reports, cost breakdowns, and CSV data downloads.
 */

window.ReportsView = class ReportsView {
    constructor() {
        this.container = document.getElementById('reports-view');
    }

    async render() {
        if (!this.container) return;

        this.container.innerHTML = `
            <div class="view-header">
                <div>
                    <h1 class="view-title"><i class="fas fa-file-export"></i> Reports & Export Hub</h1>
                    <p class="view-subtitle">Generate CSV cost reports, inventory lists, and project summaries</p>
                </div>
            </div>

            <div class="reports-grid">
                <div class="glass-card report-card">
                    <i class="fas fa-calculator report-icon"></i>
                    <h3>Budget & Cost Report</h3>
                    <p>Export itemized furniture costs, flooring, labor, and designer margins to CSV.</p>
                    <button class="btn btn-primary" onclick="window.reportsView.exportBudgetCSV()"><i class="fas fa-download"></i> Download CSV</button>
                </div>

                <div class="glass-card report-card">
                    <i class="fas fa-boxes report-icon"></i>
                    <h3>Warehouse Inventory Report</h3>
                    <p>Export complete stock levels, bin locations, and reorder alerts.</p>
                    <button class="btn btn-secondary" onclick="window.reportsView.exportInventoryCSV()"><i class="fas fa-download"></i> Download CSV</button>
                </div>
            </div>
        `;
    }

    exportBudgetCSV() {
        window.location.href = '/api/reports/budget/1/csv';
    }

    exportInventoryCSV() {
        window.location.href = '/api/reports/inventory/csv';
    }
};
