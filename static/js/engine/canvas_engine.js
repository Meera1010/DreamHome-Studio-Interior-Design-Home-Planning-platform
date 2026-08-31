/**
 * DreamHome Studio — Interactive 2D HTML5 Canvas Engine
 * High-performance 2D rendering loop, camera pan & zoom viewport, grid rendering,
 * selection highlights, object drag & transform, wall drawing, and lighting engine integration.
 */

class DHCanvasEngine {
    constructor(canvasElement) {
        this.canvas = canvasElement;
        this.ctx = this.canvas.getContext('2d');
        
        // Camera Viewport Transformation State
        this.zoom = 1.0;
        this.panX = 0;
        this.panY = 0;
        this.isPanning = false;
        this.lastMousePos = { x: 0, y: 0 };
        
        // Engine Data State
        this.roomData = {
            name: "Main Living Room",
            width_m: 8.0,
            height_m: 6.0,
            flooring_material: "Herringbone Oak Hardwood",
            wall_color: "#F5F5F0"
        };
        this.walls = [];
        this.openings = [];
        this.objects = [];
        this.lighting = [];
        this.gridSize = 20; // 20px grid
        this.scaleFactor = 50; // 50px = 1 meter
        this.showGrid = true;
        this.snapToGridEnabled = true;
        
        // Selection & Tool Mode
        this.activeTool = 'select'; // 'select', 'wall', 'door', 'window', 'light'
        this.selectedObject = null;
        this.selectedWall = null;
        this.dragState = null;
        
        // Event Subscriptions
        this.onSelectionChange = null;
        this.onCanvasModified = null;
        
        this.initViewport();
        this.bindEvents();
        this.startRenderLoop();
    }

    initViewport() {
        this.resizeCanvas();
        window.addEventListener('resize', () => this.resizeCanvas());
    }

    resizeCanvas() {
        const parent = this.canvas.parentElement;
        if (!parent) return;
        this.canvas.width = parent.clientWidth;
        this.canvas.height = parent.clientHeight;
        this.requestRender();
    }

    loadCanvasData(data) {
        if (!data) return;
        this.roomData = data.room || this.roomData;
        this.walls = data.walls || [];
        this.openings = data.openings || [];
        this.objects = data.objects || [];
        this.lighting = data.lighting || [];
        this.selectedObject = null;
        this.requestRender();
    }

    exportCanvasData() {
        return {
            room: this.roomData,
            walls: this.walls,
            openings: this.openings,
            objects: this.objects,
            lighting: this.lighting,
            scale_factor: this.scaleFactor
        };
    }

    // Convert Screen mouse coordinates to Canvas World Coordinates
    screenToWorld(screenX, screenY) {
        const rect = this.canvas.getBoundingClientRect();
        const mouseX = screenX - rect.left;
        const mouseY = screenY - rect.top;
        
        return {
            x: (mouseX - this.panX) / this.zoom,
            y: (mouseY - this.panY) / this.zoom
        };
    }

    // Convert Canvas World Coordinates to Screen Mouse Coordinates
    worldToScreen(worldX, worldY) {
        return {
            x: worldX * this.zoom + this.panX,
            y: worldY * this.zoom + this.panY
        };
    }

    setZoom(newZoom) {
        this.zoom = Math.max(0.1, Math.min(5.0, newZoom));
        this.requestRender();
    }

    setTool(toolName) {
        this.activeTool = toolName;
        this.canvas.style.cursor = toolName === 'select' ? 'default' : 'crosshair';
    }

    // Core Canvas Render Loop
    requestRender() {
        if (!this.renderRequested) {
            this.renderRequested = true;
            requestAnimationFrame(() => this.render());
        }
    }

    startRenderLoop() {
        this.requestRender();
    }

    render() {
        this.renderRequested = false;
        const ctx = this.ctx;
        const w = this.canvas.width;
        const h = this.canvas.height;

        // Clear Screen Background
        ctx.clearRect(0, 0, w, h);
        ctx.save();

        // Apply Camera Transformation (Pan & Zoom)
        ctx.translate(this.panX, this.panY);
        ctx.scale(this.zoom, this.zoom);

        // 1. Render Grid
        if (this.showGrid) {
            this.renderGrid(ctx, w, h);
        }

        // 2. Render Flooring Background Area
        this.renderFlooring(ctx);

        // 3. Render Walls
        this.renderWalls(ctx);

        // 4. Render Openings (Doors & Windows)
        this.renderOpenings(ctx);

        // 5. Render Furniture Objects
        this.renderObjects(ctx);

        // 6. Render Lighting Overlays
        this.renderLighting(ctx);

        // 7. Render Selection Handles
        if (this.selectedObject) {
            this.renderSelectionHandles(ctx, this.selectedObject);
        }

        ctx.restore();
    }

    renderGrid(ctx, screenW, screenH) {
        const gridPx = this.gridSize;
        const startX = Math.floor((-this.panX / this.zoom) / gridPx) * gridPx;
        const startY = Math.floor((-this.panY / this.zoom) / gridPx) * gridPx;
        const endX = startX + (screenW / this.zoom) + gridPx;
        const endY = startY + (screenH / this.zoom) + gridPx;

        ctx.strokeStyle = '#1e293b';
        ctx.lineWidth = 0.5;
        ctx.beginPath();

        for (let x = startX; x <= endX; x += gridPx) {
            ctx.moveTo(x, startY);
            ctx.lineTo(x, endY);
        }
        for (let y = startY; y <= endY; y += gridPx) {
            ctx.moveTo(startX, y);
            ctx.lineTo(endX, y);
        }
        ctx.stroke();
    }

    renderFlooring(ctx) {
        const roomW = (this.roomData.width_m || 8.0) * this.scaleFactor;
        const roomH = (this.roomData.height_m || 6.0) * this.scaleFactor;
        
        ctx.fillStyle = this.roomData.wall_color || '#1e293b';
        ctx.fillRect(50, 50, roomW, roomH);
        
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(50, 50, roomW, roomH);
    }

    renderWalls(ctx) {
        for (const w of this.walls) {
            ctx.strokeStyle = w.color || '#334155';
            ctx.lineWidth = w.thickness || 14;
            ctx.lineCap = 'round';
            
            ctx.beginPath();
            ctx.moveTo(w.x1, w.y1);
            ctx.lineTo(w.x2, w.y2);
            ctx.stroke();
            
            // Draw dimension text
            const dist = DHGeometry.distance({ x: w.x1, y: w.y1 }, { x: w.x2, y: w.y2 });
            const distM = (dist / this.scaleFactor).toFixed(2);
            const midX = (w.x1 + w.x2) / 2;
            const midY = (w.y1 + w.y2) / 2;
            
            ctx.fillStyle = '#94a3b8';
            ctx.font = '12px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(`${distM}m`, midX, midY - 10);
        }
    }

    renderOpenings(ctx) {
        for (const op of this.openings) {
            ctx.fillStyle = '#38bdf8';
            ctx.fillRect(op.x || 100, op.y || 100, op.width || 80, 10);
        }
    }

    renderObjects(ctx) {
        // Sort objects by z_index
        const sorted = [...this.objects].sort((a, b) => (a.z_index || 1) - (b.z_index || 1));
        
        for (const obj of sorted) {
            ctx.save();
            const centerX = obj.x + obj.width / 2;
            const centerY = obj.y + obj.depth / 2;
            
            ctx.translate(centerX, centerY);
            if (obj.rotation) {
                ctx.rotate((obj.rotation * Math.PI) / 180);
            }
            
            // Fill Furniture Box
            ctx.fillStyle = obj.color || '#6366f1';
            ctx.beginPath();
            ctx.roundRect(-obj.width / 2, -obj.depth / 2, obj.width, obj.depth, 4);
            ctx.fill();
            
            // Furniture Border Line
            ctx.strokeStyle = '#f8fafc';
            ctx.lineWidth = 1.5;
            ctx.stroke();
            
            // Label
            ctx.fillStyle = '#ffffff';
            ctx.font = '11px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(obj.name || 'Object', 0, 0);
            
            ctx.restore();
        }
    }

    renderLighting(ctx) {
        for (const l of this.lighting) {
            if (l.type === 'point') {
                const grad = ctx.createRadialGradient(l.x, l.y, 10, l.x, l.y, l.radius || 200);
                grad.addColorStop(0, 'rgba(254, 225, 128, 0.45)');
                grad.addColorStop(1, 'rgba(254, 225, 128, 0.0)');
                
                ctx.fillStyle = grad;
                ctx.beginPath();
                ctx.arc(l.x, l.y, l.radius || 200, 0, Math.PI * 2);
                ctx.fill();
            }
        }
    }

    renderSelectionHandles(ctx, obj) {
        const corners = DHGeometry.getRotatedCorners(obj.x, obj.y, obj.width, obj.depth, obj.rotation || 0);
        
        // Draw selection bounding box
        ctx.strokeStyle = '#6366f1';
        ctx.lineWidth = 2;
        ctx.setLineDash([4, 4]);
        ctx.beginPath();
        ctx.moveTo(corners[0].x, corners[0].y);
        ctx.lineTo(corners[1].x, corners[1].y);
        ctx.lineTo(corners[2].x, corners[2].y);
        ctx.lineTo(corners[3].x, corners[3].y);
        ctx.closePath();
        ctx.stroke();
        ctx.setLineDash([]);

        // Draw corner resize handles
        ctx.fillStyle = '#ffffff';
        ctx.strokeStyle = '#6366f1';
        ctx.lineWidth = 2;

        for (const corner of corners) {
            ctx.beginPath();
            ctx.arc(corner.x, corner.y, 6, 0, Math.PI * 2);
            ctx.fill();
            ctx.stroke();
        }
    }

    // Event Handling
    bindEvents() {
        this.canvas.addEventListener('mousedown', (e) => this.handleMouseDown(e));
        this.canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
        this.canvas.addEventListener('mouseup', (e) => this.handleMouseUp(e));
        this.canvas.addEventListener('wheel', (e) => this.handleWheel(e));
    }

    handleMouseDown(e) {
        const world = this.screenToWorld(e.clientX, e.clientY);
        
        if (e.button === 1 || e.spaceKey) { // Pan canvas
            this.isPanning = true;
            this.lastMousePos = { x: e.clientX, y: e.clientY };
            return;
        }

        // Check object hit selection
        let hitObject = null;
        for (let i = this.objects.length - 1; i >= 0; i--) {
            const obj = this.objects[i];
            if (DHGeometry.isPointInRotatedRect(world.x, world.y, obj.x, obj.y, obj.width, obj.depth, obj.rotation || 0)) {
                hitObject = obj;
                break;
            }
        }

        this.selectedObject = hitObject;
        if (hitObject) {
            this.dragState = {
                startX: world.x,
                startY: world.y,
                initialObjX: hitObject.x,
                initialObjY: hitObject.y
            };
        }

        if (this.onSelectionChange) {
            this.onSelectionChange(this.selectedObject);
        }

        this.requestRender();
    }

    handleMouseMove(e) {
        if (this.isPanning) {
            const dx = e.clientX - this.lastMousePos.x;
            const dy = e.clientY - this.lastMousePos.y;
            this.panX += dx;
            this.panY += dy;
            this.lastMousePos = { x: e.clientX, y: e.clientY };
            this.requestRender();
            return;
        }

        if (this.dragState && this.selectedObject) {
            const world = this.screenToWorld(e.clientX, e.clientY);
            let dx = world.x - this.dragState.startX;
            let dy = world.y - this.dragState.startY;

            let newX = this.dragState.initialObjX + dx;
            let newY = this.dragState.initialObjY + dy;

            if (this.snapToGridEnabled) {
                const snapped = DHGeometry.snapToGrid(newX, newY, this.gridSize);
                newX = snapped.x;
                newY = snapped.y;
            }

            this.selectedObject.x = newX;
            this.selectedObject.y = newY;
            
            if (this.onCanvasModified) {
                this.onCanvasModified();
            }

            this.requestRender();
        }
    }

    handleMouseUp(e) {
        this.isPanning = false;
        this.dragState = null;
    }

    handleWheel(e) {
        e.preventDefault();
        const zoomFactor = e.deltaY < 0 ? 1.1 : 0.9;
        this.setZoom(this.zoom * zoomFactor);
    }
}

window.DHCanvasEngine = DHCanvasEngine;
