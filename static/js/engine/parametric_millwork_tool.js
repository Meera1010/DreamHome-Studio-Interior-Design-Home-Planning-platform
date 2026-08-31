/**
 * DreamHome Studio — Parametric Millwork Visual Tool
 */

window.DHParametricMillworkTool = {
    init(canvasEngine) {
        this.engine = canvasEngine;
        this.cabinets = [];
    },

    addCabinet(x, y, width = 90, height = 90, depth = 60) {
        const cab = { id: 'cab_' + Date.now(), x, y, width, height, depth, doorStyle: 'Shaker' };
        this.cabinets.push(cab);
        return cab;
    },

    renderElevation(ctx, cab) {
        ctx.strokeStyle = '#6366f1';
        ctx.lineWidth = 2;
        ctx.strokeRect(cab.x, cab.y, cab.width, cab.height);
        
        // Render Shaker style inset door panel
        ctx.strokeRect(cab.x + 5, cab.y + 5, cab.width - 10, cab.height - 10);
    }
};
