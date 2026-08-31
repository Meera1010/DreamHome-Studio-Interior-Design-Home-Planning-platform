"""
DreamHome Studio — Geometry & 2D Math Service
Provides vector math, polygon room area & perimeter algorithms, wall segment intersection,
bounding box calculations, snap-to-grid alignment, and rotation transformations.
"""

import math
from typing import List, Dict, Tuple, Any, Optional

class GeometryService:
    """Mathematical utility service for 2D room design and spatial calculations."""

    @staticmethod
    def calculate_polygon_area(vertices: List[Tuple[float, float]]) -> float:
        """
        Calculate area of a 2D polygon using the Shoelace formula (Gauss's area formula).
        vertices: List of (x, y) coordinates in meters or pixels.
        Returns: Non-negative area float.
        """
        n = len(vertices)
        if n < 3:
            return 0.0
        
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += vertices[i][0] * vertices[j][1]
            area -= vertices[j][0] * vertices[i][1]
            
        return abs(area) / 2.0

    @staticmethod
    def calculate_perimeter(vertices: List[Tuple[float, float]]) -> float:
        """Calculate total perimeter length of connected 2D vertices."""
        n = len(vertices)
        if n < 2:
            return 0.0
            
        perimeter = 0.0
        for i in range(n):
            j = (i + 1) % n
            dx = vertices[j][0] - vertices[i][0]
            dy = vertices[j][1] - vertices[i][1]
            perimeter += math.sqrt(dx * dx + dy * dy)
            
        return perimeter

    @staticmethod
    def point_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """Euclidean distance between two 2D points."""
        return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

    @staticmethod
    def snap_to_grid(x: float, y: float, grid_size: float = 20.0) -> Tuple[float, float]:
        """Align (x, y) coordinates to nearest grid intersection."""
        snapped_x = round(x / grid_size) * grid_size
        snapped_y = round(y / grid_size) * grid_size
        return (snapped_x, snapped_y)

    @staticmethod
    def rotate_point(
        point: Tuple[float, float],
        center: Tuple[float, float],
        angle_degrees: float
    ) -> Tuple[float, float]:
        """Rotate a 2D point around a center origin by angle in degrees."""
        rad = math.radians(angle_degrees)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        dx = point[0] - center[0]
        dy = point[1] - center[1]
        
        rx = center[0] + (dx * cos_a - dy * sin_a)
        ry = center[1] + (dx * sin_a + dy * cos_a)
        return (round(rx, 4), round(ry, 4))

    @staticmethod
    def get_rotated_bounding_box(
        x: float,
        y: float,
        width: float,
        depth: float,
        rotation_deg: float
    ) -> List[Tuple[float, float]]:
        """
        Compute the 4 rotated corner coordinates of a rectangular furniture object.
        x, y: Top-left center position.
        width, depth: Dimensions in cm/pixels.
        rotation_deg: Rotation angle in degrees.
        Returns: List of 4 corner tuples [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        """
        center = (x + width / 2.0, y + depth / 2.0)
        unrotated_corners = [
            (x, y),
            (x + width, y),
            (x + width, y + depth),
            (x, y + depth)
        ]
        return [GeometryService.rotate_point(corner, center, rotation_deg) for corner in unrotated_corners]

    @staticmethod
    def check_line_intersection(
        line1: Tuple[Tuple[float, float], Tuple[float, float]],
        line2: Tuple[Tuple[float, float], Tuple[float, float]]
    ) -> Optional[Tuple[float, float]]:
        """
        Check if two 2D line segments intersect and return intersection point.
        line1: ((x1, y1), (x2, y2))
        line2: ((x3, y3), (x4, y4))
        """
        (x1, y1), (x2, y2) = line1
        (x3, y3), (x4, y4) = line2
        
        denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
        if denom == 0:
            return None  # Parallel lines
            
        ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
        ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom
        
        if 0.0 <= ua <= 1.0 and 0.0 <= ub <= 1.0:
            ix = x1 + ua * (x2 - x1)
            iy = y1 + ua * (y2 - y1)
            return (round(ix, 4), round(iy, 4))
            
        return None

    @staticmethod
    def calculate_room_summary_from_canvas(canvas_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract total floor area, wall length, object count, and room dimensions from canvas JSON.
        """
        walls = canvas_data.get("walls", [])
        objects = canvas_data.get("objects", [])
        openings = canvas_data.get("openings", [])
        room = canvas_data.get("room", {})
        
        width_m = float(room.get("width_m", 8.0))
        height_m = float(room.get("height_m", 6.0))
        scale = float(canvas_data.get("scale_factor", 50.0))  # 50px = 1m
        
        # Calculate wall total length in meters
        total_wall_length_m = 0.0
        wall_vertices = []
        for w in walls:
            x1, y1 = float(w.get("x1", 0)), float(w.get("y1", 0))
            x2, y2 = float(w.get("x2", 0)), float(w.get("y2", 0))
            dist_px = GeometryService.point_distance((x1, y1), (x2, y2))
            total_wall_length_m += (dist_px / scale)
            if (x1, y1) not in wall_vertices:
                wall_vertices.append((x1 / scale, y1 / scale))

        floor_area_sqm = GeometryService.calculate_polygon_area(wall_vertices)
        if floor_area_sqm == 0.0:
            floor_area_sqm = width_m * height_m

        return {
            "room_name": room.get("name", "Main Room"),
            "width_m": width_m,
            "height_m": height_m,
            "area_sqm": round(floor_area_sqm, 2),
            "area_sqft": round(floor_area_sqm * 10.7639, 2),
            "total_wall_length_m": round(total_wall_length_m, 2),
            "wall_count": len(walls),
            "furniture_count": len(objects),
            "openings_count": len(openings)
        }
