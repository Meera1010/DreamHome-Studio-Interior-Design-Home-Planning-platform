/**
 * DreamHome Studio — Client Collaboration & Feedback View Controller
 * Manages 2D canvas coordinate pins, feedback threads, and formal approval requests.
 */

window.CollaborationView = class CollaborationView {
    constructor() {
        this.container = document.getElementById('collaboration-view');
    }

    async render(floorplanId = null) {
        if (!this.container) return;

        this.container.innerHTML = `
            <div class="view-header">
                <div>
                    <h1 class="view-title"><i class="fas fa-comments"></i> Client Collaboration</h1>
                    <p class="view-subtitle">Review feedback pins, post design comments, and manage approvals</p>
                </div>
            </div>

            <div class="collaboration-layout">
                <div class="glass-card collaboration-sidebar">
                    <h3>Feedback Pins & Comments</h3>
                    <div id="comments-list" class="comments-list">
                        <div class="loading-spinner"><i class="fas fa-spinner fa-spin"></i> Loading feedback...</div>
                    </div>
                </div>

                <div class="glass-card collaboration-main">
                    <h3>Design Approval Workflow</h3>
                    <div id="approvals-container">
                        <div class="loading-spinner"><i class="fas fa-spinner fa-spin"></i> Loading approval status...</div>
                    </div>
                </div>
            </div>
        `;

        await this.loadComments(floorplanId);
    }

    async loadComments(floorplanId) {
        try {
            const url = floorplanId ? `/api/collaboration/comments?floorplan_id=${floorplanId}` : '/api/collaboration/comments';
            const response = await window.apiClient.get(url);
            const container = document.getElementById('comments-list');
            if (!container) return;

            const comments = response.comments || [];
            if (comments.length === 0) {
                container.innerHTML = `<div class="empty-state"><p>No feedback comments posted yet.</p></div>`;
                return;
            }

            container.innerHTML = comments.map(c => `
                <div class="comment-item">
                    <div class="comment-header">
                        <strong>${c.user_name || 'User'}</strong>
                        <span class="comment-time">${new Date(c.created_at).toLocaleTimeString()}</span>
                    </div>
                    <div class="comment-body">${c.content}</div>
                    ${c.pin_x ? `<div class="comment-pin-tag"><i class="fas fa-map-marker-alt"></i> Pin: (${Math.round(c.pin_x)}, ${Math.round(c.pin_y)})</div>` : ''}
                </div>
            `).join('');
        } catch (err) {
            console.error('Failed to load comments:', err);
        }
    }
};
