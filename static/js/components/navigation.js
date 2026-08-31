/**
 * DreamHome Studio — Navigation Router & Active View Dispatcher
 */

window.DHNavigation = {
    init() {
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const targetView = item.getAttribute('data-view');
                if (targetView) {
                    this.switchView(targetView);
                }
            });
        });
    },

    switchView(viewName) {
        document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
        const activeNav = document.querySelector(`.nav-item[data-view="${viewName}"]`);
        if (activeNav) activeNav.classList.add('active');

        document.querySelectorAll('.app-view').forEach(v => v.classList.add('hidden'));
        const targetSection = document.getElementById(`view-${viewName}`);
        if (targetSection) {
            targetSection.classList.remove('hidden');
        }

        const titleEl = document.getElementById('view-title');
        if (titleEl) {
            titleEl.innerText = viewName.charAt(0).toUpperCase() + viewName.slice(1).replace('-', ' ');
        }

        DHState.setState({ activeView: viewName });
        DHState.emit('viewSwitched', viewName);
    }
};
