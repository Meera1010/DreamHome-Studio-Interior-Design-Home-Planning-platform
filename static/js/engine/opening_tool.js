/**
 * DreamHome Studio — Openings Tool (Doors & Windows)
 */

window.DHOpeningTool = {
    createDoor: function(x, y, width = 80, wallId = null) {
        return {
            id: 'op_' + Date.now(),
            type: 'door',
            x: x, y: y, width: width,
            wall_id: wallId,
            swing_direction: 'inward'
        };
    },

    createWindow: function(x, y, width = 100, wallId = null) {
        return {
            id: 'op_' + Date.now(),
            type: 'window',
            x: x, y: y, width: width,
            wall_id: wallId,
            sill_height_m: 0.9
        };
    }
};
