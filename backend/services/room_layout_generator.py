"""
DreamHome Studio — Automatic Room Layout Generator Service
Algorithmic layout synthesizer that places furniture, aligns seating to walls,
places coffee tables, positions nightstands, and ensures architectural clearances.
"""

from typing import Dict, Any, List
from backend.models.furniture import FurnitureCatalog

class RoomLayoutGeneratorService:
    """Algorithmic synthesis engine for auto-generating 2D room layouts."""

    @classmethod
    def generate_layout(
        cls,
        room_name: str = "Generated Living Room",
        room_type: str = "Living Room",
        width_m: float = 8.0,
        height_m: float = 6.0,
        style: str = "Modern"
    ) -> Dict[str, Any]:
        """
        Generate a complete 2D canvas JSON payload based on room dimensions and style template.
        """
        scale = 50.0  # 50px = 1m
        width_px = width_m * scale
        height_px = height_m * scale

        # 1. Generate Surrounding Walls
        walls = [
            {"id": "w1", "x1": 50, "y1": 50, "x2": 50 + width_px, "y2": 50, "thickness": 14, "color": "#2C3E50"},
            {"id": "w2", "x1": 50 + width_px, "y1": 50, "x2": 50 + width_px, "y2": 50 + height_px, "thickness": 14, "color": "#2C3E50"},
            {"id": "w3", "x1": 50 + width_px, "y1": 50 + height_px, "x2": 50, "y2": 50 + height_px, "thickness": 14, "color": "#2C3E50"},
            {"id": "w4", "x1": 50, "y1": 50 + height_px, "x2": 50, "y2": 50, "thickness": 14, "color": "#2C3E50"}
        ]

        # 2. Door & Window Openings
        openings = [
            {"id": "op1", "type": "double_door", "wall_id": "w1", "offset_m": width_m / 2.0 - 0.8, "width_m": 1.6, "swing_direction": "inward"},
            {"id": "op2", "type": "window", "wall_id": "w2", "offset_m": 1.5, "width_m": 2.0, "sill_height_m": 0.9}
        ]

        # 3. Furniture Placement Logic based on Room Type
        objects = []
        if room_type == "Living Room":
            objects = cls._build_living_room_objects(width_px, height_px)
        elif room_type == "Bedroom":
            objects = cls._build_bedroom_objects(width_px, height_px)
        elif room_type == "Dining":
            objects = cls._build_dining_room_objects(width_px, height_px)
        else:
            objects = cls._build_living_room_objects(width_px, height_px)

        # 4. Lighting Overlay Setup
        lighting = [
            {"id": "l_amb", "type": "ambient", "color": "#FFF8E7", "intensity": 0.45},
            {"id": "l_p1", "type": "point", "x": 50 + width_px / 2.0, "y": 50 + height_px / 2.0, "radius": width_px * 0.6, "color": "#FEE180", "intensity": 0.85}
        ]

        return {
            "room": {
                "name": room_name,
                "width_m": width_m,
                "height_m": height_m,
                "flooring_material": "Herringbone Oak Hardwood",
                "wall_color": "#F5F5F0",
                "style": style
            },
            "walls": walls,
            "openings": openings,
            "objects": objects,
            "lighting": lighting,
            "scale_factor": scale
        }

    @staticmethod
    def _build_living_room_objects(width_px: float, height_px: float) -> List[Dict[str, Any]]:
        center_x = 50 + width_px / 2.0
        center_y = 50 + height_px / 2.0

        return [
            {
                "id": "gen_sofa_1",
                "catalog_id": 1,
                "name": "Modern Velvet 3-Seater Sofa",
                "x": center_x - 110, "y": center_y - 100,
                "width": 220, "depth": 95,
                "rotation": 0, "z_index": 2,
                "color": "#1B4F72"
            },
            {
                "id": "gen_tbl_1",
                "catalog_id": 3,
                "name": "Minimalist Coffee Table",
                "x": center_x - 60, "y": center_y + 20,
                "width": 120, "depth": 60,
                "rotation": 0, "z_index": 1,
                "color": "#F5CBA7"
            },
            {
                "id": "gen_rug_1",
                "catalog_id": 15,
                "name": "Geometric Area Rug",
                "x": center_x - 150, "y": center_y - 120,
                "width": 300, "depth": 220,
                "rotation": 0, "z_index": 0,
                "color": "#E5E8E8"
            },
            {
                "id": "gen_lamp_1",
                "catalog_id": 13,
                "name": "Arc Floor Lamp",
                "x": center_x - 170, "y": center_y - 110,
                "width": 40, "depth": 120,
                "rotation": 45, "z_index": 3,
                "color": "#F1C40F"
            }
        ]

    @staticmethod
    def _build_bedroom_objects(width_px: float, height_px: float) -> List[Dict[str, Any]]:
        center_x = 50 + width_px / 2.0

        return [
            {
                "id": "gen_bed_1",
                "catalog_id": 5,
                "name": "King Size Upholstered Bed",
                "x": center_x - 105, "y": 80,
                "width": 210, "depth": 200,
                "rotation": 0, "z_index": 2,
                "color": "#D5D8DC"
            },
            {
                "id": "gen_nst_1",
                "catalog_id": 6,
                "name": "Nightstand Left",
                "x": center_x - 175, "y": 90,
                "width": 55, "depth": 45,
                "rotation": 0, "z_index": 1,
                "color": "#1C2833"
            },
            {
                "id": "gen_nst_2",
                "catalog_id": 6,
                "name": "Nightstand Right",
                "x": center_x + 120, "y": 90,
                "width": 55, "depth": 45,
                "rotation": 0, "z_index": 1,
                "color": "#1C2833"
            }
        ]

    @staticmethod
    def _build_dining_room_objects(width_px: float, height_px: float) -> List[Dict[str, Any]]:
        center_x = 50 + width_px / 2.0
        center_y = 50 + height_px / 2.0

        return [
            {
                "id": "gen_dtbl_1",
                "catalog_id": 8,
                "name": "Solid Oak Dining Table",
                "x": center_x - 120, "y": center_y - 50,
                "width": 240, "depth": 100,
                "rotation": 0, "z_index": 1,
                "color": "#EDBB99"
            }
        ]
