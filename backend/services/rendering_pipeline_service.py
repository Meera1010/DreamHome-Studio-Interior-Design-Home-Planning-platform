"""
DreamHome Studio — 2D Vector Raytracing & Wall Occlusion Rendering Engine
Simulates light ray intersections, wall shadow occlusion, ambient light falloff,
and color space transformations (RGB, HSL, HEX) for high-performance canvas rendering.
"""

from typing import Dict, Any, List, Tuple
import math

class RenderingPipelineService:
    """Raytracing, occlusion shadow mapping, and color transformation engine."""

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert CSS HEX color string to RGB integer tuple."""
        hex_clean = hex_color.lstrip('#')
        if len(hex_clean) == 3:
            hex_clean = ''.join([c*2 for c in hex_clean])
        if len(hex_clean) != 6:
            return (255, 255, 255)
        return tuple(int(hex_clean[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """Convert RGB integer tuple to CSS HEX color string."""
        r_c = max(0, min(255, r))
        g_c = max(0, min(255, g))
        b_c = max(0, min(255, b))
        return f"#{r_c:02X}{g_c:02X}{b_c:02X}"

    @classmethod
    def rgb_to_hsl(cls, r: int, g: int, b: int) -> Tuple[float, float, float]:
        """Convert RGB integers to HSL (Hue 0-360, Saturation 0-1, Lightness 0-1)."""
        r_f, g_f, b_f = r / 255.0, g / 255.0, b / 255.0
        max_c = max(r_f, g_f, b_f)
        min_c = min(r_f, g_f, b_f)
        delta = max_c - min_c

        l = (max_c + min_c) / 2.0

        if delta == 0:
            h = s = 0.0
        else:
            s = delta / (1.0 - abs(2.0 * l - 1.0))
            if max_c == r_f:
                h = ((g_f - b_f) / delta) % 6
            elif max_c == g_f:
                h = ((b_f - r_f) / delta) + 2
            else:
                h = ((r_f - g_f) / delta) + 4
            h *= 60.0

        return (round(h, 1), round(s, 3), round(l, 3))

    @classmethod
    def calculate_radial_light_falloff(
        cls,
        light_x: float,
        light_y: float,
        target_x: float,
        target_y: float,
        radius: float,
        intensity: float = 1.0
    ) -> float:
        """
        Calculate inverse-square distance light intensity falloff at a specific point coordinate.
        """
        dx = target_x - light_x
        dy = target_y - light_y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist >= radius:
            return 0.0

        # Quadratic falloff curve
        attenuation = max(0.0, 1.0 - (dist / radius) ** 2)
        return round(intensity * attenuation, 3)

    @classmethod
    def trace_shadow_ray(
        cls,
        light_pos: Tuple[float, float],
        target_pos: Tuple[float, float],
        walls: List[Dict[str, Any]]
    ) -> bool:
        """
        Trace ray segment from light source to target point.
        Returns True if ray intersects any wall segment (target is in shadow/occluded).
        """
        p1_x, p1_y = light_pos
        p2_x, p2_y = target_pos

        for wall in walls:
            w1_x, w1_y = float(wall.get("x1", 0)), float(wall.get("y1", 0))
            w2_x, w2_y = float(wall.get("x2", 0)), float(wall.get("y2", 0))

            if cls._segments_intersect(p1_x, p1_y, p2_x, p2_y, w1_x, w1_y, w2_x, w2_y):
                return True # Occluded by wall

        return False

    @staticmethod
    def _segments_intersect(
        ax: float, ay: float, bx: float, by: float,
        cx: float, cy: float, dx: float, dy: float
    ) -> bool:
        """Line segment intersection test using vector cross products."""
        def ccw(x1, y1, x2, y2, x3, y3):
            return (y3 - y1) * (x2 - x1) > (y2 - y1) * (x3 - x1)

        return (ccw(ax, ay, cx, cy, dx, dy) != ccw(bx, by, cx, cy, dx, dy)) and \
               (ccw(ax, ay, bx, by, cx, cy) != ccw(ax, ay, bx, by, dx, dy))
