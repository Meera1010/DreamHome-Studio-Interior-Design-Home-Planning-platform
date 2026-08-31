/**
 * DreamHome Studio — Modal Dialog Controller
 */

window.DHModal = {
    open(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
        }
    },

    close(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('active');
        }
    },

    closeAll() {
        document.querySelectorAll('.modal-overlay.active').forEach(m => m.classList.remove('active'));
    }
};
