"""
DreamHome Studio — Floorplan SVG Export Engine
Generates vector SVG graphics string from 2D room canvas JSON data.
"""

from typing import Dict, Any

class FloorplanExporterService:
    """Renders 2D Canvas JSON layouts to standalone W3C SVG strings."""

    @staticmethod
    def export_to_svg(canvas_data: Dict[str, Any]) -> str:
        """
        Convert canvas JSON objects, walls, doors, windows, and grid into an SVG string.
        """
        room = canvas_data.get("room", {})
        walls = canvas_data.get("walls", [])
        openings = canvas_data.get("openings", [])
        objects = canvas_data.get("objects", [])

        width_m = float(room.get("width_m", 8.0))
        height_m = float(room.get("height_m", 6.0))
        scale = float(canvas_data.get("scale_factor", 50.0))

        svg_w = int(width_m * scale + 100)
        svg_h = int(height_m * scale + 100)

        svg = []
        svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">')
        svg.append('  <style>')
        svg.append('    .room-bg { fill: #ffffff; stroke: #cbd5e1; stroke-width: 2; }')
        svg.append('    .grid-line { stroke: #f1f5f9; stroke-width: 1; }')
        svg.append('    .wall { stroke: #1e293b; stroke-width: 12; stroke-linecap: round; }')
        svg.append('    .opening { stroke: #3b82f6; stroke-width: 8; fill: #ffffff; }')
        svg.append('    .furniture { stroke: #334155; stroke-width: 2; fill-opacity: 0.85; rx: 4; }')
        svg.append('    .text-label { font-family: system-ui, sans-serif; font-size: 14px; fill: #475569; text-anchor: middle; }')
        svg.append('  </style>')

        # Background & Grid
        svg.append(f'  <rect x="50" y="50" width="{width_m * scale}" height="{height_m * scale}" class="room-bg" />')

        # Draw Walls
        for w in walls:
            x1, y1 = w.get("x1", 50), w.get("y1", 50)
            x2, y2 = w.get("x2", 50), w.get("y2", 50)
            color = w.get("color", "#1e293b")
            svg.append(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="wall" stroke="{color}" />')

        # Draw Objects
        for obj in objects:
            x = obj.get("x", 0)
            y = obj.get("y", 0)
            w = obj.get("width", 50)
            d = obj.get("depth", 50)
            rot = obj.get("rotation", 0)
            name = obj.get("name", "Furniture")
            color = obj.get("color", "#64748b")

            transform = f'rotate({rot}, {x + w/2}, {y + d/2})' if rot != 0 else ''
            svg.append(f'  <g transform="{transform}">')
            svg.append(f'    <rect x="{x}" y="{y}" width="{w}" height="{d}" fill="{color}" class="furniture" />')
            svg.append(f'    <text x="{x + w/2}" y="{y + d/2 + 4}" class="text-label">{name}</text>')
            svg.append('  </g>')

        # Room Title
        room_title = room.get("name", "Room Floorplan")
        svg.append(f'  <text x="{svg_w / 2}" y="30" class="text-label" font-weight="bold" font-size="18">{room_title}</text>')
        svg.append('</svg>')

        return '\n'.join(svg)
