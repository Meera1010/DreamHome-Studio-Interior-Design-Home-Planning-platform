"""
DreamHome Studio — Architectural Lighting & Illumination Service
Calculates lumen requirements, recommended fixture counts, color temperature (Kelvin),
and energy efficiency metrics for 2D room designs.
"""

from typing import Dict, Any, List

class LightingCalculationService:
    """Illumination engineering and lumen calculation service."""

    # Lux standards per room type (Lumens per square meter)
    LUX_STANDARDS = {
        "Living Room": 150.0,
        "Bedroom": 120.0,
        "Dining": 200.0,
        "Office": 400.0,
        "Kitchen": 350.0,
        "Bathroom": 300.0
    }

    @classmethod
    def calculate_room_lighting(
        cls,
        room_type: str,
        floor_area_sqm: float,
        ceiling_height_m: float = 2.8,
        fixture_count: int = 4
    ) -> Dict[str, Any]:
        """
        Calculate total required lumens, recommended lux levels, and fixture wattage.
        """
        target_lux = cls.LUX_STANDARDS.get(room_type, 150.0)

        # Height multiplier factor
        height_factor = 1.0 + max(0.0, (ceiling_height_m - 2.5) * 0.15)
        
        total_required_lumens = round(floor_area_sqm * target_lux * height_factor, 1)

        # LED efficiency (approx 90 lumens per watt)
        estimated_total_watts = round(total_required_lumens / 90.0, 1)
        lumens_per_fixture = round(total_required_lumens / max(1, fixture_count), 1)

        kelvin_recommendation = "2700K - Warm White" if room_type in ("Living Room", "Bedroom") else "3000K - Soft White" if room_type == "Dining" else "4000K - Cool Daylight"

        return {
            "room_type": room_type,
            "floor_area_sqm": floor_area_sqm,
            "target_lux": target_lux,
            "ceiling_height_m": ceiling_height_m,
            "total_required_lumens": total_required_lumens,
            "estimated_total_watts": estimated_total_watts,
            "fixture_count": fixture_count,
            "lumens_per_fixture": lumens_per_fixture,
            "color_temperature": kelvin_recommendation
        }
