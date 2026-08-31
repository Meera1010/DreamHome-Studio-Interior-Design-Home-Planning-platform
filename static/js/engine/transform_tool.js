/**
 * DreamHome Studio — Transform Tool (Movement, Resize & 1-Degree Precision Rotation)
 */

window.DHTransformTool = {
    rotateObject: function(obj, deltaDegrees) {
        if (!obj) return;
        obj.rotation = (obj.rotation + deltaDegrees) % 360;
        if (obj.rotation < 0) obj.rotation += 360;
    },

    resizeObject: function(obj, newWidth, newDepth) {
        if (!obj) return;
        obj.width = Math.max(20, newWidth);
        obj.depth = Math.max(20, newDepth);
    }
};
