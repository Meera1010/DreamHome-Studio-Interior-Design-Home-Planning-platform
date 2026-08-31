/**
 * DreamHome Studio — Main Frontend SaaS Application Launcher
 * Initializes global state, user session check, navigation routing, and view lifecycle hooks.
 */

document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Initializing DreamHome Studio Frontend App...');

    // 1. Initialize Components
    DHThemeToggle.init();
    DHNavigation.init();
    DHAuthView.init();

    // 2. Check Active Session Profile
    try {
        let authData = await DHAPIClient.getProfile();
        if (!authData.authenticated) {
            try {
                const loginRes = await DHAPIClient.login('sarah.jenkins@dreamhome.com', 'Designer123!Password');
                authData = { authenticated: true, user: loginRes.user };
            } catch (autoLoginErr) {
                console.warn('Auto demo login skipped:', autoLoginErr);
            }
        }

        if (authData.authenticated && authData.user) {
            DHState.setState({ user: authData.user, isAuthenticated: true });
            
            // Update UI User display
            const nameEl = document.getElementById('sidebar-user-name');
            const roleEl = document.getElementById('sidebar-user-role');
            const avatarEl = document.getElementById('sidebar-user-avatar');
            if (nameEl) nameEl.innerText = authData.user.full_name;
            if (roleEl) roleEl.innerText = authData.user.role;
            if (avatarEl && authData.user.avatar_url) avatarEl.src = authData.user.avatar_url;

            // Trigger Dashboard Data Load
            DHDashboardView.init();
        } else {
            DHModal.open('auth-modal');
        }
    } catch (err) {
        console.warn('Session check failed, opening login prompt');
        DHModal.open('auth-modal');
    }

    // 3. Listen to View Switch Events to Initialize Module Views
    DHState.on('viewSwitched', (viewName) => {
        switch (viewName) {
            case 'dashboard':
                DHDashboardView.init();
                break;
            case 'designer':
                if (!DHDesignerView.canvasEngine) {
                    DHDesignerView.init();
                }
                break;
            case 'projects':
                DHProjectsView.init();
                break;
            case 'budget':
                DHBudgetView.init();
                break;
            case 'inventory':
                DHInventoryView.init();
                break;
            case 'tasks':
                DHTasksView.init();
                break;
            case 'admin':
                DHAdminView.init();
                break;
        }
    });

    // 4. Trigger Initial View (Dashboard)
    DHDashboardView.init();
});
