/**
 * DreamHome Studio — Texture & Material Manager
 */

window.DHTextureManager = {
    applyFlooring: function(roomData, material) {
        if (!roomData || !material) return;
        roomData.flooring_material = material.name;
    },

    applyWallColor: function(roomData, colorHex) {
        if (!roomData) return;
        roomData.wall_color = colorHex;
    }
};
