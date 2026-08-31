/**
 * DreamHome Studio — Warehouse Inventory View Controller
 */

window.DHInventoryView = {
    async init() {
        const tbody = document.getElementById('inventory-tbody');
        if (!tbody) return;

        try {
            const data = await DHAPIClient.request('/api/inventory');
            const items = data.inventory || [];

            tbody.innerHTML = items.map(item => `
                <tr>
                    <td><code>${item.sku || 'N/A'}</code></td>
                    <td><strong>${item.furniture_name}</strong></td>
                    <td>${item.supplier_name}</td>
                    <td><strong style="color:${item.quantity_in_stock <= item.reorder_level ? 'var(--danger)' : 'var(--text-primary)'}">${item.quantity_in_stock}</strong></td>
                    <td>$${item.unit_cost.toFixed(2)}</td>
                    <td>${item.bin_location || 'BIN-01'}</td>
                    <td><span class="badge ${item.quantity_in_stock <= item.reorder_level ? 'badge-danger' : 'badge-success'}">${item.status}</span></td>
                </tr>
            `).join('');

        } catch (err) {
            tbody.innerHTML = '<tr><td colspan="7" style="color:var(--danger);">Failed to load inventory data</td></tr>';
        }
    }
};
