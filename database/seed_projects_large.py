"""
DreamHome Studio — Extended Multi-Room Floorplan Canvas Seed Generator
Generates realistic multi-room architectural floorplans with complete 2D canvas JSON payloads,
wall segments, doors, windows, lighting nodes, and furniture object layouts.
"""

import json
from typing import Dict, Any, List

def generate_multi_room_floorplan_json(room_title: str, room_type: str) -> str:
    """Generate complete 2D Canvas JSON representation for multi-room layouts."""
    
    # 8m x 6m room (400px x 300px at 50px/m scale)
    width_m = 8.0
    height_m = 6.0
    scale = 50.0

    walls = [
        {"id": "w1", "x1": 50, "y1": 50, "x2": 450, "y2": 50, "thickness": 14, "color": "#2C3E50"},
        {"id": "w2", "x1": 450, "y1": 50, "x2": 450, "y2": 350, "thickness": 14, "color": "#2C3E50"},
        {"id": "w3", "x1": 450, "y1": 350, "x2": 50, "y2": 350, "thickness": 14, "color": "#2C3E50"},
        {"id": "w4", "x1": 50, "y1": 350, "x2": 50, "y2": 50, "thickness": 14, "color": "#2C3E50"}
    ]

    openings = [
        {"id": "op1", "type": "double_door", "wall_id": "w1", "offset_m": 3.2, "width_m": 1.6, "swing_direction": "inward"},
        {"id": "op2", "type": "window", "wall_id": "w2", "offset_m": 1.5, "width_m": 2.0, "sill_height_m": 0.9},
        {"id": "op3", "type": "window", "wall_id": "w4", "offset_m": 1.5, "width_m": 1.5, "sill_height_m": 0.9}
    ]

    objects = []
    if "Living" in room_type:
        objects = [
            {"id": "obj_sofa", "catalog_id": 1, "name": "Nordic Velvet 3-Seater Sofa", "x": 140, "y": 100, "width": 220, "depth": 95, "rotation": 0, "z_index": 2, "color": "#1B4F72"},
            {"id": "obj_tbl", "catalog_id": 3, "name": "Marble Coffee Table", "x": 190, "y": 220, "width": 120, "depth": 60, "rotation": 0, "z_index": 1, "color": "#FFFFFF"},
            {"id": "obj_rug", "catalog_id": 15, "name": "Geometric Area Rug", "x": 100, "y": 90, "width": 300, "depth": 220, "rotation": 0, "z_index": 0, "color": "#E5E8E8"},
            {"id": "obj_lamp", "catalog_id": 13, "name": "Brushed Brass Arc Lamp", "x": 80, "y": 90, "width": 45, "depth": 125, "rotation": 45, "z_index": 3, "color": "#F1C40F"}
        ]
    elif "Bedroom" in room_type:
        objects = [
            {"id": "obj_bed", "catalog_id": 5, "name": "King Size Upholstered Bed", "x": 145, "y": 80, "width": 210, "depth": 200, "rotation": 0, "z_index": 2, "color": "#D5D8DC"},
            {"id": "obj_nst1", "catalog_id": 6, "name": "Nightstand Left", "x": 80, "y": 90, "width": 55, "depth": 45, "rotation": 0, "z_index": 1, "color": "#1C2833"},
            {"id": "obj_nst2", "catalog_id": 6, "name": "Nightstand Right", "x": 365, "y": 90, "width": 55, "depth": 45, "rotation": 0, "z_index": 1, "color": "#1C2833"},
            {"id": "obj_drs", "catalog_id": 7, "name": "Executive 6-Drawer Dresser", "x": 170, "y": 290, "width": 160, "depth": 50, "rotation": 0, "z_index": 1, "color": "#F5CBA7"}
        ]
    else:
        objects = [
            {"id": "obj_dtbl", "catalog_id": 8, "name": "Solid Oak Dining Table", "x": 130, "y": 150, "width": 240, "depth": 100, "rotation": 0, "z_index": 1, "color": "#EDBB99"},
            {"id": "obj_dchr1", "catalog_id": 9, "name": "Dining Chair 1", "x": 150, "y": 90, "width": 50, "depth": 52, "rotation": 0, "z_index": 2, "color": "#F2F4F4"},
            {"id": "obj_dchr2", "catalog_id": 9, "name": "Dining Chair 2", "x": 220, "y": 90, "width": 50, "depth": 52, "rotation": 0, "z_index": 2, "color": "#F2F4F4"}
        ]

    lighting = [
        {"id": "l_amb", "type": "ambient", "color": "#FFF8E7", "intensity": 0.5},
        {"id": "l_p1", "type": "point", "x": 250, "y": 200, "radius": 250, "color": "#FEE180", "intensity": 0.85}
    ]

    payload = {
        "room": {
            "name": room_title,
            "width_m": width_m,
            "height_m": height_m,
            "ceiling_height_m": 2.8,
            "flooring_material": "Herringbone Oak Hardwood",
            "wall_color": "#F5F5F0"
        },
        "walls": walls,
        "openings": openings,
        "objects": objects,
        "lighting": lighting,
        "scale_factor": scale
    }

    return json.dumps(payload)
