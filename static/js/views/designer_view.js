/**
 * DreamHome Studio — 2D Interactive Room Designer View Controller
 */

window.DHDesignerView = {
    canvasEngine: null,
    historyManager: null,

    init() {
        const canvasEl = document.getElementById('room-canvas');
        if (!canvasEl) return;

        // Initialize Canvas Engine and History Stack
        this.canvasEngine = new DHCanvasEngine(canvasEl);
        this.historyManager = new DHHistoryManager();

        // Subscribe Canvas selection changes to Property Inspector
        this.canvasEngine.onSelectionChange = (selectedObj) => {
            DHPropertyInspector.render(selectedObj, this.canvasEngine);
        };

        this.canvasEngine.onCanvasModified = () => {
            this.historyManager.pushState(this.canvasEngine.exportCanvasData());
            this.updateUndoRedoButtons();
        };

        // Load Catalog Items into Drawer
        DHCatalogBrowser.loadCatalog('catalog-items-grid', this.canvasEngine);

        // Bind Toolbar Buttons
        this.bindToolbarEvents();

        // Load Default Sample Layout (Floorplan 1)
        this.loadSampleFloorplan(1);
    },

    async loadSampleFloorplan(floorplanId) {
        try {
            const res = await DHAPIClient.getFloorplan(floorplanId);
            if (res.floorplan && res.floorplan.canvas_data) {
                this.canvasEngine.loadCanvasData(res.floorplan.canvas_data);
                this.historyManager.pushState(res.floorplan.canvas_data);
                this.updateUndoRedoButtons();
            }
        } catch (err) {
            console.error('Failed to load sample floorplan:', err);
        }
    },

    bindToolbarEvents() {
        // Tool Buttons
        document.querySelectorAll('.tool-btn[data-tool]').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.tool-btn[data-tool]').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const tool = btn.getAttribute('data-tool');
                this.canvasEngine.setTool(tool);
            });
        });

        // Zoom Buttons
        document.getElementById('btn-zoom-in')?.addEventListener('click', () => {
            this.canvasEngine.setZoom(this.canvasEngine.zoom * 1.2);
        });

        document.getElementById('btn-zoom-out')?.addEventListener('click', () => {
            this.canvasEngine.setZoom(this.canvasEngine.zoom * 0.8);
        });

        document.getElementById('btn-zoom-reset')?.addEventListener('click', () => {
            this.canvasEngine.zoom = 1.0;
            this.canvasEngine.panX = 0;
            this.canvasEngine.panY = 0;
            this.canvasEngine.requestRender();
        });

        // Undo / Redo Buttons
        document.getElementById('btn-undo')?.addEventListener('click', () => {
            const prevState = this.historyManager.undo(this.canvasEngine.exportCanvasData());
            if (prevState) {
                this.canvasEngine.loadCanvasData(prevState);
                this.updateUndoRedoButtons();
            }
        });

        document.getElementById('btn-redo')?.addEventListener('click', () => {
            const nextState = this.historyManager.redo(this.canvasEngine.exportCanvasData());
            if (nextState) {
                this.canvasEngine.loadCanvasData(nextState);
                this.updateUndoRedoButtons();
            }
        });

        // Export Buttons
        document.getElementById('btn-export-png')?.addEventListener('click', () => {
            DHExporter.exportToPNG(this.canvasEngine.canvas, 'dreamhome_floorplan.png');
        });

        document.getElementById('btn-export-json')?.addEventListener('click', () => {
            DHExporter.exportToJSON(this.canvasEngine, 'dreamhome_floorplan.json');
        });

        // Save Floorplan Button
        document.getElementById('btn-save-canvas')?.addEventListener('click', async () => {
            try {
                const data = this.canvasEngine.exportCanvasData();
                await DHAPIClient.saveFloorplanCanvas(1, data, 'Saved Layout Update');
                if (window.DHToast) window.DHToast.success('Floorplan saved to database!');
            } catch (err) {
                if (window.DHToast) window.DHToast.error('Failed to save floorplan');
            }
        });
    },

    updateUndoRedoButtons() {
        const undoBtn = document.getElementById('btn-undo');
        const redoBtn = document.getElementById('btn-redo');
        if (undoBtn) undoBtn.disabled = !this.historyManager.canUndo();
        if (redoBtn) redoBtn.disabled = !this.historyManager.canRedo();
    }
};
