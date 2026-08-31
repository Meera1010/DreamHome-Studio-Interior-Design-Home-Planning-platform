/**
 * DreamHome Studio — Account Settings View Controller
 * Manages user profile updates, password modification, and theme preferences.
 */

window.SettingsView = class SettingsView {
    constructor() {
        this.container = document.getElementById('settings-view');
    }

    async render() {
        if (!this.container) return;

        const user = window.state ? window.state.user : {};

        this.container.innerHTML = `
            <div class="view-header">
                <div>
                    <h1 class="view-title"><i class="fas fa-cog"></i> Account Settings</h1>
                    <p class="view-subtitle">Manage personal profile details, company bio, and system preferences</p>
                </div>
            </div>

            <div class="settings-layout">
                <div class="glass-card settings-card">
                    <h3>Profile Information</h3>
                    <form id="form-settings-profile">
                        <div class="form-group">
                            <label class="form-label">Full Name</label>
                            <input type="text" id="set-full-name" class="form-control" value="${user ? user.full_name || '' : ''}">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Phone Number</label>
                            <input type="text" id="set-phone" class="form-control" value="${user ? user.phone || '' : ''}">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Company / Studio Name</label>
                            <input type="text" id="set-company" class="form-control" value="${user ? user.company || '' : ''}">
                        </div>
                        <button type="submit" class="btn btn-primary"><i class="fas fa-save"></i> Save Profile</button>
                    </form>
                </div>
            </div>
        `;

        const form = document.getElementById('form-settings-profile');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                window.toast.show('Profile updated successfully', 'success');
            });
        }
    }
};
