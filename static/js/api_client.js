/**
 * DreamHome Studio — REST API Client Wrapper
 * Encapsulates fetch HTTP calls, error handling, JSON body parsing, and auth headers.
 */

window.DHAPIClient = {
    async request(url, options = {}) {
        const defaultHeaders = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        };

        const config = {
            ...options,
            headers: {
                ...defaultHeaders,
                ...options.headers
            }
        };

        if (config.body && typeof config.body === 'object') {
            config.body = JSON.stringify(config.body);
        }

        try {
            const response = await fetch(url, config);
            const data = await response.json().catch(() => ({}));

            if (!response.ok) {
                const errorMsg = data.error || `HTTP ${response.status} Error`;
                if (window.DHToast && response.status !== 401) {
                    window.DHToast.error(errorMsg);
                }
                throw new Error(errorMsg);
            }

            return data;
        } catch (err) {
            console.error(`API Error [${url}]:`, err.message);
            throw err;
        }
    },

    // Auth endpoints
    login(email, password) {
        return this.request('/api/auth/login', { method: 'POST', body: { email, password } });
    },
    register(userData) {
        return this.request('/api/auth/register', { method: 'POST', body: userData });
    },
    logout() {
        return this.request('/api/auth/logout', { method: 'POST' });
    },
    getProfile() {
        return this.request('/api/auth/me', { method: 'GET' });
    },

    // Projects endpoints
    getProjects(status = null) {
        const query = status ? `?status=${encodeURIComponent(status)}` : '';
        return this.request(`/api/projects${query}`, { method: 'GET' });
    },
    getProject(id) {
        return this.request(`/api/projects/${id}`, { method: 'GET' });
    },
    createProject(data) {
        return this.request('/api/projects', { method: 'POST', body: data });
    },

    // Floorplans endpoints
    getProjectFloorplans(projectId) {
        return this.request(`/api/floorplans/project/${projectId}`, { method: 'GET' });
    },
    getFloorplan(id) {
        return this.request(`/api/floorplans/${id}`, { method: 'GET' });
    },
    createFloorplan(data) {
        return this.request('/api/floorplans', { method: 'POST', body: data });
    },
    saveFloorplanCanvas(id, canvasData, title = null) {
        return this.request(`/api/floorplans/${id}/save`, { method: 'POST', body: { canvas_data: canvasData, title } });
    },

    // Catalog endpoints
    getFurniture(category = null, query = null) {
        let params = [];
        if (category) params.push(`category=${encodeURIComponent(category)}`);
        if (query) params.push(`q=${encodeURIComponent(query)}`);
        const qStr = params.length > 0 ? `?${params.join('&')}` : '';
        return this.request(`/api/catalog/furniture${qStr}`, { method: 'GET' });
    },
    getMaterials(category = null) {
        const qStr = category ? `?category=${encodeURIComponent(category)}` : '';
        return this.request(`/api/catalog/materials${qStr}`, { method: 'GET' });
    },

    // Analytics & Admin endpoints
    getDashboardAnalytics() {
        return this.request('/api/analytics/dashboard', { method: 'GET' });
    },
    getAdminUsers() {
        return this.request('/api/admin/users', { method: 'GET' });
    },
    getAuditLogs() {
        return this.request('/api/admin/audit-logs', { method: 'GET' });
    }
};
