/**
 * DreamHome Studio — Toast Notification Component
 */

window.DHToast = {
    show(message, type = 'info', duration = 4000) {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <span>${message}</span>
            <button style="background:none;border:none;color:inherit;cursor:pointer;" onclick="this.parentElement.remove()">✕</button>
        `;

        container.appendChild(toast);

        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, duration);
    },

    success(message) { this.show(message, 'success'); },
    warning(message) { this.show(message, 'warning'); },
    error(message) { this.show(message, 'danger'); },
    info(message) { this.show(message, 'info'); }
};
