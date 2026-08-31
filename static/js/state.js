/**
 * DreamHome Studio — Central State Management & Event Bus
 */

class DHStateStore {
    constructor() {
        this.state = {
            user: null,
            isAuthenticated: false,
            activeView: 'dashboard',
            activeProject: null,
            activeFloorplan: null,
            theme: 'dark'
        };
        this.listeners = {};
    }

    getState() {
        return this.state;
    }

    setState(newState) {
        this.state = { ...this.state, ...newState };
        this.emit('stateChanged', this.state);
    }

    on(event, callback) {
        if (!this.listeners[event]) {
            this.listeners[event] = [];
        }
        this.listeners[event].push(callback);
    }

    emit(event, data) {
        if (this.listeners[event]) {
            this.listeners[event].forEach(cb => cb(data));
        }
    }
}

window.DHState = new DHStateStore();
