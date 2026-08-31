/**
 * DreamHome Studio — Auth View Controller (Login & Registration Forms)
 */

window.DHAuthView = {
    init() {
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            loginForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const email = document.getElementById('login-email').value;
                const password = document.getElementById('login-password').value;

                try {
                    const res = await DHAPIClient.login(email, password);
                    DHState.setState({ user: res.user, isAuthenticated: true });
                    DHModal.close('auth-modal');
                    if (window.DHToast) window.DHToast.success(`Welcome back, ${res.user.full_name}!`);
                    location.reload();
                } catch (err) {
                    console.error('Login failed:', err);
                }
            });
        }
    }
};
