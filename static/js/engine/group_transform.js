/**
 * DreamHome Studio — Group Selection & Multi-Object Transform Engine
 * Enables multi-object marquee selection, bounding box group scaling, and group translation.
 */

window.GroupTransformEngine = class GroupTransformEngine {
    constructor() {
        this.selectedObjects = [];
        this.groupBounds = null;
    }

    setGroup(objects) {
        this.selectedObjects = objects || [];
        this.calculateBounds();
    }

    calculateBounds() {
        if (this.selectedObjects.length === 0) {
            this.groupBounds = null;
            return;
        }

        let minX = Infinity, minY = Infinity;
        let maxX = -Infinity, maxY = -Infinity;

        this.selectedObjects.forEach(obj => {
            minX = Math.min(minX, obj.x);
            minY = Math.min(minY, obj.y);
            maxX = Math.max(maxX, obj.x + obj.width);
            maxY = Math.max(maxY, obj.y + obj.depth);
        });

        this.groupBounds = {
            x: minX,
            y: minY,
            width: maxX - minX,
            depth: maxY - minY
        };
    }

    translateGroup(dx, dy) {
        if (!this.groupBounds) return;
        this.selectedObjects.forEach(obj => {
            obj.x += dx;
            obj.y += dy;
        });
        this.calculateBounds();
    }

    renderGroupBoundingBox(ctx, camera) {
        if (!this.groupBounds || this.selectedObjects.length < 2) return;

        ctx.save();
        ctx.strokeStyle = '#6366F1';
        ctx.lineWidth = 2 / camera.zoom;
        ctx.setLineDash([6, 6]);

        ctx.strokeRect(
            this.groupBounds.x - 5,
            this.groupBounds.y - 5,
            this.groupBounds.width + 10,
            this.groupBounds.depth + 10
        );

        ctx.restore();
    }
};
