/**
 * DreamHome Studio — Portfolio Showcase View Controller
 * Displays public designer showcases, hero imagery, view counters, and client inquiry forms.
 */

window.PortfolioView = class PortfolioView {
    constructor() {
        this.container = document.getElementById('portfolio-view');
    }

    async render() {
        if (!this.container) return;

        this.container.innerHTML = `
            <div class="view-header">
                <div>
                    <h1 class="view-title"><i class="fas fa-briefcase"></i> Designer Portfolio</h1>
                    <p class="view-subtitle">Showcase completed interior design projects to prospective clients</p>
                </div>
            </div>

            <div class="portfolio-gallery-grid" id="portfolio-gallery">
                <div class="loading-spinner"><i class="fas fa-spinner fa-spin"></i> Loading portfolio showcases...</div>
            </div>
        `;

        await this.loadPortfolios();
    }

    async loadPortfolios() {
        try {
            const response = await window.apiClient.get('/api/portfolios');
            const container = document.getElementById('portfolio-gallery');
            if (!container) return;

            const items = response.portfolios || [];
            if (items.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <i class="fas fa-camera empty-icon"></i>
                        <h3>No Portfolios Published</h3>
                        <p>Publish your completed floorplan projects to build your public portfolio gallery.</p>
                    </div>
                `;
                return;
            }

            container.innerHTML = items.map(p => `
                <div class="glass-card portfolio-card">
                    <div class="portfolio-image-wrapper">
                        <img src="${p.hero_image_url || '/static/images/projects/coastal_villa.jpg'}" alt="${p.title}" class="portfolio-img">
                        <span class="portfolio-style-badge">${p.style_tag || 'Modern'}</span>
                    </div>
                    <div class="portfolio-card-content">
                        <h3>${p.title}</h3>
                        <p>${p.description || ''}</p>
                        <div class="portfolio-stats">
                            <span><i class="fas fa-eye"></i> ${p.view_count || 0} Views</span>
                            <span><i class="fas fa-heart"></i> ${p.like_count || 0} Likes</span>
                        </div>
                    </div>
                </div>
            `).join('');
        } catch (err) {
            console.error('Failed to load portfolio items:', err);
        }
    }
};
