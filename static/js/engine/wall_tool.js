/**
 * DreamHome Studio — Interactive Wall Drawing & Room Enclosure Tool
 * Allows designers to click-and-drag or point-to-point draw architectural walls.
 */

window.DHWallTool = {
    /**
     * Create a new wall segment.
     */
    createWall: function(x1, y1, x2, y2, thickness = 14, color = '#334155') {
        return {
            id: 'wall_' + Date.now() + '_' + Math.floor(Math.random() * 1000),
            x1: Math.round(x1),
            y1: Math.round(y1),
            x2: Math.round(x2),
            y2: Math.round(y2),
            thickness: thickness,
            color: color
        };
    },

    /**
     * Calculate wall length in meters based on canvas scale factor.
     */
    getWallLengthMeters: function(wall, scaleFactor = 50) {
        const distPx = DHGeometry.distance({ x: wall.x1, y: wall.y1 }, { x: wall.x2, y: wall.y2 });
        return (distPx / scaleFactor).toFixed(2);
    }
};
