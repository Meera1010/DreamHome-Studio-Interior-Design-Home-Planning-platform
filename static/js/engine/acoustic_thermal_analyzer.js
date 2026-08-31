/**
 * DreamHome Studio — Acoustic & Thermal Analyzer Canvas Overlay
 */

window.DHAcousticThermalAnalyzer = {
    init(canvasEngine) {
        this.engine = canvasEngine;
    },

    renderAcousticRays(ctx, sourceX, sourceY, rayCount = 12) {
        ctx.strokeStyle = 'rgba(239, 68, 68, 0.4)';
        ctx.lineWidth = 1;
        for (let i = 0; i < rayCount; i++) {
            const angle = (i / rayCount) * Math.PI * 2;
            ctx.beginPath();
            ctx.moveTo(sourceX, sourceY);
            ctx.lineTo(sourceX + Math.cos(angle) * 150, sourceY + Math.sin(angle) * 150);
            ctx.stroke();
        }
    }
};
