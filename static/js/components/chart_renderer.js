/**
 * DreamHome Studio — Pure Vanilla JS SVG & Canvas Chart Engine
 * Renders SVG Bar charts, Donut charts, and Line graphs without external libraries.
 */

window.DHChartRenderer = {
    renderBarChart(containerId, dataSeries) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const width = container.clientWidth || 300;
        const height = 220;
        const padding = 30;

        const maxVal = Math.max(...dataSeries.map(d => d.value), 1);
        const barWidth = (width - padding * 2) / dataSeries.length - 10;

        let svg = `<svg width="100%" height="${height}" viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg">`;
        
        dataSeries.forEach((d, i) => {
            const x = padding + i * (barWidth + 10);
            const barH = (d.value / maxVal) * (height - padding * 2);
            const y = height - padding - barH;
            const color = d.color || '#6366f1';

            svg += `<rect x="${x}" y="${y}" width="${barWidth}" height="${barH}" fill="${color}" rx="4" />`;
            svg += `<text x="${x + barWidth / 2}" y="${height - 10}" fill="#94a3b8" font-size="11" text-anchor="middle">${d.label}</text>`;
            svg += `<text x="${x + barWidth / 2}" y="${y - 6}" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">${d.value}</text>`;
        });

        svg += `</svg>`;
        container.innerHTML = svg;
    },

    renderDonutChart(containerId, dataSeries) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const size = 200;
        const radius = 70;
        const circumference = 2 * Math.PI * radius;
        const total = dataSeries.reduce((acc, d) => acc + d.value, 0) || 1;

        let currentOffset = 0;
        let svg = `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">`;

        dataSeries.forEach(d => {
            const strokeDash = (d.value / total) * circumference;
            const strokeDasharray = `${strokeDash} ${circumference - strokeDash}`;
            const strokeDashoffset = -currentOffset;
            const color = d.color || '#6366f1';

            svg += `<circle cx="${size/2}" cy="${size/2}" r="${radius}" fill="transparent" stroke="${color}" stroke-width="24" stroke-dasharray="${strokeDasharray}" stroke-dashoffset="${strokeDashoffset}" transform="rotate(-90 ${size/2} ${size/2})" />`;
            currentOffset += strokeDash;
        });

        svg += `<text x="${size/2}" y="${size/2 + 4}" fill="#f8fafc" font-size="16" font-weight="bold" text-anchor="middle">${total}</text>`;
        svg += `</svg>`;

        container.innerHTML = svg;
    }
};
