/**
 * DreamHome Studio — Dynamic Property Inspector Panel Controller
 */

window.DHPropertyInspector = {
    render(selectedObject, canvasEngine) {
        const container = document.getElementById('inspector-content');
        if (!container) return;

        if (!selectedObject) {
            container.innerHTML = `
                <div style="text-align:center; padding: 2rem 1rem; color: var(--text-muted);">
                    <p>No item selected</p>
                    <small>Click any furniture object, wall, or light on canvas to edit properties.</small>
                </div>
            `;
            return;
        }

        container.innerHTML = `
            <div class="form-group">
                <label class="form-label">Item Name</label>
                <input type="text" id="prop-name" class="form-input" value="${selectedObject.name || ''}">
            </div>
            <div class="form-group">
                <label class="form-label">Width (cm)</label>
                <input type="number" id="prop-width" class="form-input" value="${selectedObject.width || 100}">
            </div>
            <div class="form-group">
                <label class="form-label">Depth (cm)</label>
                <input type="number" id="prop-depth" class="form-input" value="${selectedObject.depth || 80}">
            </div>
            <div class="form-group">
                <label class="form-label">Rotation (°)</label>
                <input type="range" id="prop-rotation" min="0" max="360" class="form-input" value="${selectedObject.rotation || 0}">
                <span id="rotation-val" style="font-size:0.8rem;color:var(--text-secondary);">${selectedObject.rotation || 0}°</span>
            </div>
            <div class="form-group">
                <label class="form-label">Color / Finish</label>
                <input type="color" id="prop-color" class="form-input" value="${selectedObject.color || '#6366f1'}" style="height:40px;padding:2px;">
            </div>
            <div style="display:flex;gap:0.5rem;margin-top:1rem;">
                <button id="btn-front" class="btn btn-secondary btn-sm" style="flex:1;">Bring Front</button>
                <button id="btn-back" class="btn btn-secondary btn-sm" style="flex:1;">Send Back</button>
            </div>
            <button id="btn-delete" class="btn btn-danger btn-sm" style="width:100%;margin-top:0.75rem;">Delete Object</button>
        `;

        // Bind Inspectors Inputs to Live Canvas Object Mutations
        document.getElementById('prop-name').addEventListener('input', (e) => {
            selectedObject.name = e.target.value;
            canvasEngine.requestRender();
        });

        document.getElementById('prop-width').addEventListener('change', (e) => {
            selectedObject.width = parseFloat(e.target.value) || 100;
            canvasEngine.requestRender();
        });

        document.getElementById('prop-depth').addEventListener('change', (e) => {
            selectedObject.depth = parseFloat(e.target.value) || 80;
            canvasEngine.requestRender();
        });

        document.getElementById('prop-rotation').addEventListener('input', (e) => {
            selectedObject.rotation = parseInt(e.target.value) || 0;
            document.getElementById('rotation-val').innerText = `${selectedObject.rotation}°`;
            canvasEngine.requestRender();
        });

        document.getElementById('prop-color').addEventListener('input', (e) => {
            selectedObject.color = e.target.value;
            canvasEngine.requestRender();
        });

        document.getElementById('btn-front').addEventListener('click', () => {
            DHObjectManager.bringToFront(canvasEngine.objects, selectedObject);
            canvasEngine.requestRender();
        });

        document.getElementById('btn-back').addEventListener('click', () => {
            DHObjectManager.sendToBack(canvasEngine.objects, selectedObject);
            canvasEngine.requestRender();
        });

        document.getElementById('btn-delete').addEventListener('click', () => {
            canvasEngine.objects = canvasEngine.objects.filter(o => o.id !== selectedObject.id);
            canvasEngine.selectedObject = null;
            this.render(null, canvasEngine);
            canvasEngine.requestRender();
        });
    }
};
