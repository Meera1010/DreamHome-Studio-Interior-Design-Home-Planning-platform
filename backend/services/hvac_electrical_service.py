"""
DreamHome Studio — HVAC & Electrical CAD Analysis Service
Calculates duct airflow CFM requirements, electrical circuit load balancing,
and breaker panel capacity.
"""

from typing import List, Dict, Any

class HVACElectricalService:
    """Service for HVAC duct airflow and electrical load distribution."""

    @staticmethod
    def calculate_room_cfm(room_area_sqm: float, ceiling_height_m: float = 2.8, air_changes_per_hour: float = 6.0) -> Dict[str, Any]:
        """Calculate Cubic Feet per Minute (CFM) required for room HVAC airflow."""
        volume_m3 = room_area_sqm * ceiling_height_m
        volume_cu_ft = volume_m3 * 35.3147
        total_cfh = volume_cu_ft * air_changes_per_hour
        required_cfm = total_cfh / 60.0
        
        # Determine duct diameter
        duct_diameter_inches = 6
        if required_cfm > 400:
            duct_diameter_inches = 12
        elif required_cfm > 250:
            duct_diameter_inches = 10
        elif required_cfm > 120:
            duct_diameter_inches = 8
            
        return {
            "room_area_sqm": room_area_sqm,
            "volume_m3": round(volume_m3, 2),
            "required_cfm": round(required_cfm, 1),
            "recommended_duct_diameter_inches": duct_diameter_inches,
            "air_changes_per_hour": air_changes_per_hour
        }

    @staticmethod
    def calculate_circuit_load(fixtures: List[Dict[str, Any]], voltage: float = 120.0) -> Dict[str, Any]:
        """Audit electrical circuit wattage, current draw, and breaker size."""
        total_wattage = sum(f.get("watts", 60.0) for f in fixtures)
        amperage = total_wattage / voltage
        
        # 80% continuous load safety factor (NEC standard)
        recommended_breaker_amps = 15 if amperage < 12 else 20 if amperage < 16 else 30
        
        return {
            "total_fixtures": len(fixtures),
            "total_wattage": round(total_wattage, 1),
            "current_draw_amps": round(amperage, 2),
            "recommended_breaker_amps": recommended_breaker_amps,
            "capacity_utilized_percent": round((amperage / recommended_breaker_amps) * 100.0, 1),
            "nec_compliant": amperage <= (recommended_breaker_amps * 0.8)
        }
