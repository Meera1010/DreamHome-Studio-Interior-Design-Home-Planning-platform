/**
 * DreamHome Studio — Furniture Object & Layer Manager
 */

window.DHObjectManager = {
    createFurnitureObject: function(catalogItem, posX = 200, posY = 200) {
        return {
            id: 'obj_' + Date.now() + '_' + Math.floor(Math.random() * 1000),
            catalog_id: catalogItem.id,
            name: catalogItem.name,
            x: posX,
            y: posY,
            width: catalogItem.width_cm || 100,
            depth: catalogItem.depth_cm || 80,
            rotation: 0,
            z_index: catalogItem.default_z_index || 1,
            color: (catalogItem.color_options && catalogItem.color_options[0]) || '#6366f1',
            material: catalogItem.material || 'Standard',
            price: catalogItem.price || 0.0
        };
    },

    bringToFront: function(objects, selectedObj) {
        if (!selectedObj) return;
        const maxZ = Math.max(...objects.map(o => o.z_index || 1), 1);
        selectedObj.z_index = maxZ + 1;
    },

    sendToBack: function(objects, selectedObj) {
        if (!selectedObj) return;
        const minZ = Math.min(...objects.map(o => o.z_index || 1), 1);
        selectedObj.z_index = Math.max(0, minZ - 1);
    }
};
