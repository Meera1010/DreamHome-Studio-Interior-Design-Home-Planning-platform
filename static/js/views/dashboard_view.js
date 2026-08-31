/**
 * DreamHome Studio — Dashboard View Controller
 */

window.DHDashboardView = {
    async init() {
        try {
            const data = await DHAPIClient.getDashboardAnalytics();
            const analytics = data.analytics || {};
            const kpis = analytics.kpis || {};

            // Render KPI values
            document.getElementById('kpi-projects-count').innerText = kpis.total_projects || 0;
            document.getElementById('kpi-active-count').innerText = kpis.active_projects || 0;
            document.getElementById('kpi-budget-total').innerText = `$${(kpis.total_estimated_budget || 0).toLocaleString()}`;
            document.getElementById('kpi-floorplans-count').innerText = kpis.total_floorplans || 0;

            // Render Status Chart
            const breakdown = analytics.project_status_breakdown || {};
            const chartSeries = Object.keys(breakdown).map((status, idx) => ({
                label: status,
                value: breakdown[status],
                color: ['#6366f1', '#10b981', '#f59e0b', '#06b6d4', '#ef4444'][idx % 5]
            }));

            if (chartSeries.length > 0) {
                DHChartRenderer.renderBarChart('chart-project-status', chartSeries);
            }

            // Render Recent Activities
            const activityList = document.getElementById('recent-activity-list');
            if (activityList && analytics.recent_activities) {
                activityList.innerHTML = analytics.recent_activities.map(act => `
                    <div style="padding:0.65rem 0;border-bottom:1px solid var(--border-light);display:flex;align-items:center;justify-content:space-between;font-size:0.85rem;">
                        <div>
                            <strong>${act.user_name || 'System'}</strong> performed <span class="text-accent">${act.action}</span> on ${act.entity_type}
                        </div>
                        <span class="text-muted" style="font-size:0.75rem;">${new Date(act.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
                    </div>
                `).join('');
            }

        } catch (err) {
            console.error('Failed to initialize dashboard view:', err);
        }
    }
};
