/**
 * DreamHome Studio — Canvas Layout Exporter (PNG & JSON)
 */

window.DHExporter = {
    exportToPNG: function(canvasElement, fileName = 'floorplan_export.png') {
        const link = document.createElement('a');
        link.download = fileName;
        link.href = canvasElement.toDataURL('image/png');
        link.click();
    },

    exportToJSON: function(canvasEngine, fileName = 'floorplan_data.json') {
        const data = canvasEngine.exportCanvasData();
        const jsonStr = JSON.stringify(data, null, 2);
        const blob = new Blob([jsonStr], { type: 'application/json' });
        const link = document.createElement('a');
        link.download = fileName;
        link.href = URL.createObjectURL(blob);
        link.click();
    }
};
