/**
 * DreamHome Studio — Projects View Controller
 */

window.DHProjectsView = {
    async init() {
        const grid = document.getElementById('projects-grid-container');
        if (!grid) return;

        grid.innerHTML = '<div style="color:var(--text-muted);">Loading projects...</div>';

        try {
            const data = await DHAPIClient.getProjects();
            const projects = data.projects || [];

            if (projects.length === 0) {
                grid.innerHTML = '<div style="color:var(--text-muted);">No projects found. Click "New Project" to start one.</div>';
                return;
            }

            grid.innerHTML = projects.map(p => `
                <div class="project-card">
                    <img src="${p.cover_image || '/static/images/projects/default_cover.jpg'}" class="project-cover" alt="${p.title}" onerror="this.src='/static/images/projects/default_cover.jpg'">
                    <div class="project-body">
                        <div class="flex-row justify-between items-center">
                            <span class="badge badge-info">${p.status}</span>
                            <span style="font-weight:700;color:var(--accent-primary); font-size:0.9rem;">$${p.budget_limit.toLocaleString()}</span>
                        </div>
                        <h3 class="project-title">${p.title}</h3>
                        <p style="font-size:0.85rem;line-clamp:2;">${p.description || 'No description'}</p>
                        <div class="project-meta">
                            <span>Client: ${p.client_name || 'Unassigned'}</span>
                            <span>Target: ${p.target_completion_date || 'N/A'}</span>
                        </div>
                        <div style="margin-top:auto;padding-top:0.75rem;display:flex;gap:0.5rem;">
                            <button class="btn btn-primary btn-sm open-designer-btn" data-id="${p.id}" style="flex:1;">Open 2D Studio</button>
                        </div>
                    </div>
                </div>
            `).join('');

            // Bind Open 2D Studio Click Listeners
            grid.querySelectorAll('.open-designer-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    DHNavigation.switchView('designer');
                });
            });

        } catch (err) {
            grid.innerHTML = '<div style="color:var(--danger);">Failed to load projects.</div>';
        }
    }
};
