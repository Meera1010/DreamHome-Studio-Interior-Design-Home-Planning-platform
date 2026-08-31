/**
 * DreamHome Studio — Admin Panel View Controller
 */

window.DHAdminView = {
    async init() {
        const usersTbody = document.getElementById('admin-users-tbody');
        const auditTbody = document.getElementById('admin-audit-tbody');
        if (!usersTbody) return;

        try {
            const usersData = await DHAPIClient.getAdminUsers();
            const users = usersData.users || [];

            usersTbody.innerHTML = users.map(u => `
                <tr>
                    <td>#${u.id}</td>
                    <td><strong>${u.full_name}</strong></td>
                    <td>${u.email}</td>
                    <td><span class="badge badge-info">${u.role}</span></td>
                    <td><span class="badge ${u.is_active ? 'badge-success' : 'badge-danger'}">${u.is_active ? 'Active' : 'Disabled'}</span></td>
                    <td>
                        <button class="btn btn-outline btn-sm role-btn" data-id="${u.id}">Change Role</button>
                    </td>
                </tr>
            `).join('');

            const auditData = await DHAPIClient.getAuditLogs();
            const logs = auditData.audit_logs || [];

            if (auditTbody) {
                auditTbody.innerHTML = logs.map(l => `
                    <tr>
                        <td>${new Date(l.created_at).toLocaleString()}</td>
                        <td>${l.user_name || 'System'}</td>
                        <td><code style="color:var(--accent-primary);">${l.action}</code></td>
                        <td>${l.entity_type} #${l.entity_id || ''}</td>
                        <td><small style="color:var(--text-muted);">${JSON.stringify(l.details || {})}</small></td>
                    </tr>
                `).join('');
            }

        } catch (err) {
            console.error('Failed to load admin panel:', err);
        }
    }
};
