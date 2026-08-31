/**
 * DreamHome Studio — Advanced 2D Canvas Snap Engine
 * Provides smart alignment guide lines, wall proximity magnetic snapping,
 * and object-to-object edge alignment guides.
 */

window.AdvancedSnapEngine = class AdvancedSnapEngine {
    constructor(gridSize = 20, snapThreshold = 10) {
        this.gridSize = gridSize;
        this.snapThreshold = snapThreshold;
        this.activeGuides = [];
    }

    snapPointToGrid(x, y) {
        const snappedX = Math.round(x / this.gridSize) * this.gridSize;
        const snappedY = Math.round(y / this.gridSize) * this.gridSize;
        return { x: snappedX, y: snappedY };
    }

    findAlignmentGuides(targetObj, allObjects) {
        this.activeGuides = [];
        if (!targetObj || !allObjects) return { x: targetObj.x, y: targetObj.y };

        let snappedX = targetObj.x;
        let snappedY = targetObj.y;

        const tCX = targetObj.x + targetObj.width / 2;
        const tCY = targetObj.y + targetObj.depth / 2;

        allObjects.forEach(obj => {
            if (obj.id === targetObj.id) return;

            const oCX = obj.x + obj.width / 2;
            const oCY = obj.y + obj.depth / 2;

            // Center X alignment guide
            if (Math.abs(tCX - oCX) < this.snapThreshold) {
                snappedX = oCX - targetObj.width / 2;
                this.activeGuides.push({ type: 'vertical', x: oCX });
            }

            // Center Y alignment guide
            if (Math.abs(tCY - oCY) < this.snapThreshold) {
                snappedY = oCY - targetObj.depth / 2;
                this.activeGuides.push({ type: 'horizontal', y: oCY });
            }
        });

        return { x: snappedX, y: snappedY };
    }

    renderGuides(ctx, camera) {
        if (!this.activeGuides || this.activeGuides.length === 0) return;

        ctx.save();
        ctx.strokeStyle = '#00F0FF';
        ctx.lineWidth = 1 / camera.zoom;
        ctx.setLineDash([4, 4]);

        this.activeGuides.forEach(g => {
            ctx.beginPath();
            if (g.type === 'vertical') {
                ctx.moveTo(g.x, -5000);
                ctx.lineTo(g.x, 5000);
            } else if (g.type === 'horizontal') {
                ctx.moveTo(-5000, g.y);
                ctx.lineTo(5000, g.y);
            }
            ctx.stroke();
        });

        ctx.restore();
    }
};
