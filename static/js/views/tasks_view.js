/**
 * DreamHome Studio — Task Board View Controller
 */

window.DHTasksView = {
    async init() {
        const container = document.getElementById('tasks-board-container');
        if (!container) return;

        try {
            const data = await DHAPIClient.request('/api/tasks/project/1');
            const tasks = data.tasks || [];

            container.innerHTML = tasks.map(task => `
                <div class="glass-panel" style="padding:1rem;margin-bottom:0.75rem;">
                    <div class="flex-row justify-between items-center" style="margin-bottom:0.4rem;">
                        <span class="badge ${task.priority === 'High' || task.priority === 'Urgent' ? 'badge-danger' : 'badge-info'}">${task.priority}</span>
                        <small class="text-muted">Due: ${task.due_date || 'N/A'}</small>
                    </div>
                    <h4 style="font-size:0.95rem;margin-bottom:0.25rem;">${task.title}</h4>
                    <p style="font-size:0.8rem;margin-bottom:0.5rem;">${task.description || ''}</p>
                    <div class="flex-row justify-between items-center" style="font-size:0.75rem;color:var(--text-secondary);">
                        <span>Assignee: ${task.assignee_name || 'Unassigned'}</span>
                        <span class="badge badge-success">${task.status}</span>
                    </div>
                </div>
            `).join('');

        } catch (err) {
            container.innerHTML = '<div style="color:var(--danger);">Failed to load tasks.</div>';
        }
    }
};
