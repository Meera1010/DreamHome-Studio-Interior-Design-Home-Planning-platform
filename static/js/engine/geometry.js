/**
 * DreamHome Studio — Client 2D Geometry & Math Library
 * Handles vector calculations, grid snapping, polygon area/perimeter formulas,
 * line intersections, and rotation matrices.
 */

window.DHGeometry = {
    /**
     * Snap x, y coordinates to nearest grid unit.
     */
    snapToGrid: function(x, y, gridSize = 20) {
        return {
            x: Math.round(x / gridSize) * gridSize,
            y: Math.round(y / gridSize) * gridSize
        };
    },

    /**
     * Distance between two 2D points.
     */
    distance: function(p1, p2) {
        const dx = p2.x - p1.x;
        const dy = p2.y - p1.y;
        return Math.sqrt(dx * dx + dy * dy);
    },

    /**
     * Rotate point around center origin by angle in degrees.
     */
    rotatePoint: function(point, center, angleDeg) {
        const rad = (angleDeg * Math.PI) / 180;
        const cosA = Math.cos(rad);
        const sinA = Math.sin(rad);

        const dx = point.x - center.x;
        const dy = point.y - center.y;

        return {
            x: center.x + (dx * cosA - dy * sinA),
            y: center.y + (dx * sinA + dy * cosA)
        };
    },

    /**
     * Compute 4 rotated corners of a bounding rectangle.
     */
    getRotatedCorners: function(x, y, width, depth, rotationDeg) {
        const center = { x: x + width / 2, y: y + depth / 2 };
        const corners = [
            { x: x, y: y },
            { x: x + width, y: y },
            { x: x + width, y: y + depth },
            { x: x, y: y + depth }
        ];

        return corners.map(c => this.rotatePoint(c, center, rotationDeg));
    },

    /**
     * Calculate area of a polygon using Shoelace formula.
     */
    calculatePolygonArea: function(vertices) {
        const n = vertices.length;
        if (n < 3) return 0;

        let area = 0;
        for (let i = 0; i < n; i++) {
            const j = (i + 1) % n;
            area += vertices[i].x * vertices[j].y;
            area -= vertices[j].x * vertices[i].y;
        }

        return Math.abs(area) / 2.0;
    },

    /**
     * Check if point (px, py) is inside a rotated rectangle.
     */
    isPointInRotatedRect: function(px, py, rectX, rectY, width, depth, rotationDeg) {
        const center = { x: rectX + width / 2, y: rectY + depth / 2 };
        // Rotate test point inversely
        const unrotatedPoint = this.rotatePoint({ x: px, y: py }, center, -rotationDeg);

        return (
            unrotatedPoint.x >= rectX &&
            unrotatedPoint.x <= rectX + width &&
            unrotatedPoint.y >= rectY &&
            unrotatedPoint.y <= rectY + depth
        );
    }
};
