/**
 * DreamHome Studio — Budget Management & Cost Calculator View Controller
 */

window.DHBudgetView = {
    async init() {
        const tableBody = document.getElementById('budget-items-tbody');
        if (!tableBody) return;

        try {
            const data = await DHAPIClient.request('/api/budgets/project/1');
            const budget = data.budget || {};
            const items = budget.line_items || [];

            document.getElementById('budget-stat-est').innerText = `$${(budget.total_estimated || 0).toLocaleString()}`;
            document.getElementById('budget-stat-spent').innerText = `$${(budget.total_spent || 0).toLocaleString()}`;

            if (items.length === 0) {
                tableBody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:var(--text-muted);">No line items found</td></tr>';
                return;
            }

            tableBody.innerHTML = items.map(item => `
                <tr>
                    <td><strong>${item.item_name}</strong></td>
                    <td>${item.category}</td>
                    <td>$${item.unit_price.toFixed(2)}</td>
                    <td>${item.quantity}</td>
                    <td><strong>$${item.total_price.toFixed(2)}</strong></td>
                    <td><span class="badge ${item.status === 'Purchased' ? 'badge-success' : 'badge-info'}">${item.status}</span></td>
                </tr>
            `).join('');

        } catch (err) {
            console.error('Failed to load budget details:', err);
        }
    }
};
