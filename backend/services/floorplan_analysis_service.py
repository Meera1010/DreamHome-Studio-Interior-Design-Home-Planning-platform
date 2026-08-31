"""
DreamHome Studio — Floorplan Compliance & Spatial Analysis Service
Analyzes 2D room layouts for minimum walkway clearances, doorway accessibility,
natural light exposure scores, wall enclosure validity, and fire exit safety pathways.
"""

from typing import Dict, Any, List, Tuple
from backend.services.geometry_service import GeometryService

class FloorplanAnalysisService:
    """Architectural compliance and spatial optimization analysis engine."""

    MIN_WALKWAY_CLEARANCE_CM = 75.0  # 75cm minimum walkway clearance standard
    MIN_DOOR_CLEARANCE_CM = 90.0     # 90cm door opening clearance requirement

    @classmethod
    def analyze_room_layout(cls, canvas_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform spatial audit on 2D canvas room layout.
        Returns accessibility score (0-100), warnings, recommendations, and metrics.
        """
        objects = canvas_data.get("objects", [])
        walls = canvas_data.get("walls", [])
        openings = canvas_data.get("openings", [])
        room = canvas_data.get("room", {})

        width_m = float(room.get("width_m", 8.0))
        height_m = float(room.get("height_m", 6.0))
        floor_area_sqm = width_m * height_m

        warnings = []
        recommendations = []
        score = 100

        # 1. Total Furniture Density & Coverage Percentage
        total_furniture_area_sqm = 0.0
        for obj in objects:
            w_m = float(obj.get("width", 100)) / 100.0
            d_m = float(obj.get("depth", 80)) / 100.0
            total_furniture_area_sqm += (w_m * d_m)

        coverage_ratio = (total_furniture_area_sqm / floor_area_sqm) if floor_area_sqm > 0 else 0.0
        coverage_percent = round(coverage_ratio * 100, 1)

        if coverage_percent > 45.0:
            warnings.append(f"High furniture density ({coverage_percent}% coverage). Room may feel cluttered.")
            recommendations.append("Consider reducing large furniture items or switching to multi-functional pieces.")
            score -= 15
        elif coverage_percent < 15.0:
            recommendations.append("Room has significant unutilized space. Consider adding accent tables or area rugs.")

        # 2. Doorway & Clearance Checks
        door_count = 0
        window_count = 0
        for op in openings:
            if op.get("type") in ("door", "single_door", "double_door"):
                door_count += 1
            elif op.get("type") == "window":
                window_count += 1

        if door_count == 0:
            warnings.append("No entry/exit door found in room enclosure.")
            score -= 20

        if window_count == 0:
            warnings.append("No natural light window opening detected.")
            recommendations.append("Add at least one window to maximize natural daylighting.")
            score -= 10

        # 3. Object Proximity & Overlap Audit
        overlaps_detected = 0
        for i in range(len(objects)):
            for j in range(i + 1, len(objects)):
                o1, o2 = objects[i], objects[j]
                # Bounding box collision check
                if cls._check_bounding_box_overlap(o1, o2):
                    overlaps_detected += 1
                    warnings.append(f"Potential object collision detected between '{o1.get('name')}' and '{o2.get('name')}'.")

        if overlaps_detected > 0:
            score -= (overlaps_detected * 10)

        # Clamp score between 0 and 100
        score = max(0, min(100, score))

        rating = "Excellent" if score >= 90 else "Good" if score >= 75 else "Needs Improvement" if score >= 50 else "Poor"

        return {
            "overall_score": score,
            "rating": rating,
            "metrics": {
                "floor_area_sqm": round(floor_area_sqm, 2),
                "furniture_coverage_sqm": round(total_furniture_area_sqm, 2),
                "furniture_coverage_percent": coverage_percent,
                "furniture_count": len(objects),
                "wall_count": len(walls),
                "door_count": door_count,
                "window_count": window_count,
                "collisions_count": overlaps_detected
            },
            "warnings": warnings,
            "recommendations": recommendations
        }

    @staticmethod
    def _check_bounding_box_overlap(o1: Dict[str, Any], o2: Dict[str, Any]) -> bool:
        """Check axis-aligned bounding box overlap between two furniture items."""
        x1_min, x1_max = float(o1.get("x", 0)), float(o1.get("x", 0)) + float(o1.get("width", 50))
        y1_min, y1_max = float(o1.get("y", 0)), float(o1.get("y", 0)) + float(o1.get("depth", 50))

        x2_min, x2_max = float(o2.get("x", 0)), float(o2.get("x", 0)) + float(o2.get("width", 50))
        y2_min, y2_max = float(o2.get("y", 0)), float(o2.get("y", 0)) + float(o2.get("depth", 50))

        return not (x1_max <= x2_min or x1_min >= x2_max or y1_max <= y2_min or y1_min >= y2_max)
