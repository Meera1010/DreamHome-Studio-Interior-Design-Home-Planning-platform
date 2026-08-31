"""
DreamHome Studio — Moodboard Generator & Color Swatch Service
Extracts dominant color palettes from floorplan furniture objects and materials,
and auto-arranges design moodboard collage grid templates.
"""

from typing import Dict, Any, List

class MoodboardGeneratorService:
    """Automated moodboard layout and color palette extraction engine."""

    @staticmethod
    def extract_color_palette(canvas_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Extract dominant color swatches from canvas furniture objects and materials.
        """
        objects = canvas_data.get("objects", [])
        room = canvas_data.get("room", {})
        
        swatches = []

        # Wall color
        wall_color = room.get("wall_color", "#F5F5F0")
        swatches.append({"hex": wall_color, "label": "Wall Color"})

        # Furniture colors
        seen_colors = set()
        seen_colors.add(wall_color.upper())

        for obj in objects:
            color = obj.get("color", "#6366f1").upper()
            name = obj.get("name", "Furniture")
            if color not in seen_colors:
                seen_colors.add(color)
                swatches.append({"hex": color, "label": f"{name} Accent"})

        return swatches[:6] # Max 6 color swatches

    @staticmethod
    def build_default_moodboard_grid(title: str, swatches: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Build grid layout configuration for a new moodboard.
        """
        items = []

        # Main hero inspiration image item
        items.append({
            "id": "item_hero",
            "type": "image",
            "src": "/static/images/moodboards/hero_inspiration.jpg",
            "span_cols": 2,
            "span_rows": 2
        })

        # Color swatch grid items
        for idx, swatch in enumerate(swatches):
            items.append({
                "id": f"item_color_{idx}",
                "type": "color",
                "hex": swatch["hex"],
                "label": swatch["label"],
                "span_cols": 1,
                "span_rows": 1
            })

        return {
            "title": title,
            "items": items
        }
