/**
 * DreamHome Studio — Moodboard Builder View Controller
 * Manages interactive moodboard grid collages, image uploads, color palette swatches,
 * and inspiration card arrangements.
 */

window.MoodboardView = class MoodboardView {
    constructor() {
        this.container = document.getElementById('moodboard-view');
        this.activeMoodboard = null;
    }

    async render(projectId = null) {
        if (!this.container) return;

        this.container.innerHTML = `
            <div class="view-header">
                <div>
                    <h1 class="view-title"><i class="fas fa-palette"></i> Design Moodboards</h1>
                    <p class="view-subtitle">Curate inspiration collages, color swatches, and material palettes</p>
                </div>
                <div class="view-actions">
                    <button class="btn btn-primary" id="btn-create-moodboard"><i class="fas fa-plus"></i> New Moodboard</button>
                </div>
            </div>

            <div class="moodboard-grid" id="moodboards-container">
                <div class="loading-spinner"><i class="fas fa-spinner fa-spin"></i> Loading moodboards...</div>
            </div>
        `;

        this.bindEvents();
        await this.loadMoodboards(projectId);
    }

    bindEvents() {
        const btnCreate = document.getElementById('btn-create-moodboard');
        if (btnCreate) {
            btnCreate.addEventListener('click', () => this.showCreateModal());
        }
    }

    async loadMoodboards(projectId) {
        try {
            const url = projectId ? `/api/moodboards?project_id=${projectId}` : '/api/moodboards';
            const response = await window.apiClient.get(url);
            const container = document.getElementById('moodboards-container');
            
            if (!container) return;

            const moodboards = response.moodboards || [];
            if (moodboards.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <i class="fas fa-palette empty-icon"></i>
                        <h3>No Moodboards Created</h3>
                        <p>Create your first design moodboard collage to organize visual ideas.</p>
                        <button class="btn btn-primary" onclick="document.getElementById('btn-create-moodboard').click()">Create Moodboard</button>
                    </div>
                `;
                return;
            }

            container.innerHTML = moodboards.map(m => `
                <div class="glass-card moodboard-card" data-id="${m.id}">
                    <div class="moodboard-card-header">
                        <h3>${m.title}</h3>
                        <span class="badge badge-info">${m.project_title || 'General'}</span>
                    </div>
                    <div class="moodboard-swatches">
                        ${this.renderSwatches(m.items_json)}
                    </div>
                    <div class="moodboard-card-footer">
                        <span><i class="fas fa-clock"></i> ${new Date(m.created_at).toLocaleDateString()}</span>
                        <button class="btn btn-sm btn-outline" onclick="window.moodboardView.openMoodboard(${m.id})">Open Board</button>
                    </div>
                </div>
            `).join('');
        } catch (err) {
            console.error('Failed to load moodboards:', err);
            window.toast.show('Failed to load moodboards', 'error');
        }
    }

    renderSwatches(itemsJson) {
        try {
            const items = typeof itemsJson === 'string' ? JSON.parse(itemsJson) : itemsJson;
            if (!Array.isArray(items)) return '<div class="swatch-placeholder">No items</div>';

            const colorItems = items.filter(i => i.type === 'color');
            return colorItems.map(c => `
                <div class="color-swatch-chip" style="background-color: ${c.hex};" title="${c.label || c.hex}"></div>
            `).join('');
        } catch (e) {
            return '<div class="swatch-placeholder">Custom Collage</div>';
        }
    }

    showCreateModal() {
        window.modal.show({
            title: 'Create Design Moodboard',
            content: `
                <form id="form-create-moodboard">
                    <div class="form-group">
                        <label class="form-label">Moodboard Title</label>
                        <input type="text" id="mb-title" class="form-control" placeholder="e.g. Coastal Living Room Aesthetic" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Description / Theme</label>
                        <textarea id="mb-description" class="form-control" rows="3" placeholder="Warm neutral tones, natural wood, brushed brass accents..."></textarea>
                    </div>
                </form>
            `,
            confirmText: 'Create Moodboard',
            onConfirm: async () => {
                const title = document.getElementById('mb-title').value.trim();
                const description = document.getElementById('mb-description').value.trim();
                if (!title) return false;

                try {
                    await window.apiClient.post('/api/moodboards', { title, description });
                    window.toast.show('Moodboard created successfully', 'success');
                    await this.loadMoodboards();
                    return true;
                } catch (err) {
                    window.toast.show('Failed to create moodboard', 'error');
                    return false;
                }
            }
        });
    }

    openMoodboard(id) {
        window.toast.show(`Opening Moodboard #${id}`, 'info');
    }
};
