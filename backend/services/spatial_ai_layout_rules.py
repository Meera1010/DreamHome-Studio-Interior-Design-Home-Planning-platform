"""
DreamHome Studio — Spatial AI & Rule-Based Interior Optimization
Computes ergonomic clearances, traffic flow vectors, HSV color harmony indices,
Feng Shui energy balance scores, and acoustic sound reflections.
"""

import math
from typing import List, Dict, Any, Tuple

class SpatialAILayoutRules:
    """Rule-based interior spatial design optimization service."""

    @staticmethod
    def evaluate_ergonomic_clearance(furniture_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Audit clearance zones around beds, desks, sofas, and dining tables."""
        violations = []
        for i, f1 in enumerate(furniture_items):
            for j, f2 in enumerate(furniture_items):
                if i >= j:
                    continue
                x1, y1 = f1.get("x", 0), f1.get("y", 0)
                x2, y2 = f2.get("x", 0), f2.get("y", 0)
                
                dist_cm = math.hypot(x2 - x1, y2 - y1)
                min_clearance = 90.0  # 90cm default clearance standard
                
                cat1 = f1.get("category", "")
                cat2 = f2.get("category", "")
                if "Bed" in cat1 or "Bed" in cat2:
                    min_clearance = 75.0
                elif "Dining" in cat1 or "Dining" in cat2:
                    min_clearance = 100.0  # Space to pull out chairs
                    
                if dist_cm < min_clearance:
                    violations.append({
                        "item_1": f1.get("name"),
                        "item_2": f2.get("name"),
                        "actual_distance_cm": round(dist_cm, 1),
                        "required_clearance_cm": min_clearance,
                        "severity": "WARNING_TIGHT_WALKWAY"
                    })
        return violations

    @staticmethod
    def calculate_feng_shui_balance(room_layout: Dict[str, Any]) -> Dict[str, Any]:
        """Compute Feng Shui spatial balance index based on door alignment and natural light."""
        bed_or_desk = room_layout.get("primary_item", {})
        doors = room_layout.get("doors", [])
        windows = room_layout.get("windows", [])
        
        commanding_position = True
        for door in doors:
            # Check if bed/desk is directly in line with door
            if abs(bed_or_desk.get("x", 0) - door.get("x", 0)) < 40:
                commanding_position = False
                
        score = 85 if commanding_position else 55
        if len(windows) > 0:
            score += 10
            
        return {
            "commanding_position": commanding_position,
            "feng_shui_score": min(100, score),
            "rating": "HARMONIOUS" if score >= 80 else "NEEDS_OPTIMIZATION",
            "recommendation": "Maintain clear line of sight to room entryway without direct alignment."
        }
