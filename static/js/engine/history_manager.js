/**
 * DreamHome Studio — Undo & Redo History Stack Manager
 */

class DHHistoryManager {
    constructor(maxHistory = 50) {
        this.undoStack = [];
        this.redoStack = [];
        this.maxHistory = maxHistory;
    }

    pushState(stateData) {
        // Deep clone state snapshot
        const snapshot = JSON.parse(JSON.stringify(stateData));
        this.undoStack.push(snapshot);
        if (this.undoStack.length > this.maxHistory) {
            this.undoStack.shift();
        }
        this.redoStack = []; // Clear redo stack on new action
    }

    undo(currentState) {
        if (this.undoStack.length === 0) return null;
        const currentSnapshot = JSON.parse(JSON.stringify(currentState));
        this.redoStack.push(currentSnapshot);
        return this.undoStack.pop();
    }

    redo(currentState) {
        if (this.redoStack.length === 0) return null;
        const currentSnapshot = JSON.parse(JSON.stringify(currentState));
        this.undoStack.push(currentSnapshot);
        return this.redoStack.pop();
    }

    canUndo() {
        return this.undoStack.length > 0;
    }

    canRedo() {
        return this.redoStack.length > 0;
    }
}

window.DHHistoryManager = DHHistoryManager;
