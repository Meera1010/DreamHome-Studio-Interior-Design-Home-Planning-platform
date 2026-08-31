/**
 * DreamHome Studio — Lighting System Manager
 */

window.DHLightingEngine = {
    addPointLight: function(lightingArray, x, y, radius = 200, color = '#FEE180', intensity = 0.85) {
        const light = {
            id: 'light_' + Date.now(),
            type: 'point',
            x: x,
            y: y,
            radius: radius,
            color: color,
            intensity: intensity
        };
        lightingArray.push(light);
        return light;
    }
};
