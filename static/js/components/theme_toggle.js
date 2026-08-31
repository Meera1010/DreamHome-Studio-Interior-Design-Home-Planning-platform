/**
 * DreamHome Studio — Dark / Light Mode Theme Switcher Component
 */

window.DHThemeToggle = {
    init() {
        const toggleBtn = document.getElementById('theme-toggle-btn');
        if (!toggleBtn) return;

        const currentTheme = localStorage.getItem('dh_theme') || 'dark';
        document.documentElement.setAttribute('data-theme', currentTheme);

        toggleBtn.addEventListener('click', () => {
            const theme = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('dh_theme', theme);
            DHState.setState({ theme });
        });
    }
};
