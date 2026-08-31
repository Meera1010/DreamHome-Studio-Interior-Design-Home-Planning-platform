"""
DreamHome Studio — Acoustic & Thermal Performance Analyzer
Computes room reverberation time (RT60) using Sabine's formula,
wall assembly thermal R-values, and HVAC heating/cooling BTU loads.
"""

import math
from typing import List, Dict, Any

class AcousticThermalAnalysisService:
    """Service for architectural acoustics and thermal insulation performance."""

    @staticmethod
    def calculate_sabine_rt60(room_volume_m3: float, surface_areas: Dict[str, float], absorption_coefficients: Dict[str, float]) -> Dict[str, Any]:
        """Compute Reverberation Time (RT60) using Sabine's equation: RT60 = 0.161 * V / total_sabins."""
        total_sabins = 0.0
        for surface, area in surface_areas.items():
            coef = absorption_coefficients.get(surface, 0.05)
            total_sabins += area * coef
            
        rt60_seconds = (0.161 * room_volume_m3) / max(total_sabins, 0.1)
        
        acoustic_quality = "Optimal Speech Clarity" if 0.4 <= rt60_seconds <= 0.7 else "Excessive Echo" if rt60_seconds > 1.0 else "Dead Acoustics"
        
        return {
            "room_volume_m3": room_volume_m3,
            "total_sabins": round(total_sabins, 2),
            "rt60_seconds": round(rt60_seconds, 2),
            "acoustic_quality": acoustic_quality,
            "target_rt60_range": "0.4s - 0.7s (Residential/Office Standard)"
        }

    @staticmethod
    def calculate_wall_r_value(layers: List[Dict[str, float]]) -> Dict[str, Any]:
        """Calculate total thermal resistance (R-value) of multi-layer wall assembly."""
        total_r = sum(layer.get("r_value", 1.0) for layer in layers)
        u_factor = 1.0 / max(total_r, 0.1)  # U-factor = 1 / R
        
        return {
            "layer_count": len(layers),
            "total_r_value": round(total_r, 2),
            "overall_u_factor": round(u_factor, 4),
            "energy_code_compliant": total_r >= 19.0  # IECC Climate Zone standard
        }
