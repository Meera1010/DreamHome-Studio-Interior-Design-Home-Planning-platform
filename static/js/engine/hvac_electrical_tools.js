/**
 * DreamHome Studio — HVAC & Electrical 2D Tool
 */

window.DHHVACElectricalTool = {
    init(canvasEngine) {
        this.engine = canvasEngine;
        this.outlets = [];
        this.vents = [];
    },

    addOutlet(x, y, voltage = 120) {
        const outlet = { id: 'out_' + Date.now(), x, y, voltage, watts: 180 };
        this.outlets.push(outlet);
        return outlet;
    },

    addVent(x, y, cfm = 150) {
        const vent = { id: 'vnt_' + Date.now(), x, y, cfm, ductSize: 8 };
        this.vents.push(vent);
        return vent;
    },

    render(ctx) {
        this.outlets.forEach(o => {
            ctx.fillStyle = '#f59e0b';
            ctx.beginPath();
            ctx.arc(o.x, o.y, 6, 0, Math.PI * 2);
            ctx.fill();
        });
        this.vents.forEach(v => {
            ctx.strokeStyle = '#06b6d4';
            ctx.lineWidth = 2;
            ctx.strokeRect(v.x - 10, v.y - 10, 20, 20);
        });
    }
};
