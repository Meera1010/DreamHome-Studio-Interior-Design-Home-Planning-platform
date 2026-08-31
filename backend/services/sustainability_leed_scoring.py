"""
DreamHome Studio — LEED Sustainability Scoring & Environmental Impact Service
Provides LEED v4 Interior Design & Construction (ID+C) credit evaluation,
volatile organic compound (VOC) emissions verification, recycled material ratio calculations,
and energy consumption modeling.
"""

from typing import List, Dict, Any

class SustainabilityLEEDScoringService:
    """LEED certification and environmental compliance engine."""

    LEED_CREDIT_CATEGORIES = {
        "LOCATION_TRANSPORTATION": 18,
        "WATER_EFFICIENCY": 12,
        "ENERGY_ATMOSPHERE": 38,
        "MATERIALS_RESOURCES": 20,
        "INDOOR_ENVIRONMENTAL_QUALITY": 17,
        "INNOVATION_DESIGN": 6,
        "REGIONAL_PRIORITY": 4
    }

    @staticmethod
    def evaluate_materials_credits(materials: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate Materials & Resources (MR) credits based on recycled content and FSC wood certified products."""
        total_material_cost = sum(m.get("cost", 0.0) for m in materials) or 1.0
        recycled_cost = sum(m.get("cost", 0.0) for m in materials if m.get("is_recycled", False))
        fsc_wood_cost = sum(m.get("cost", 0.0) for m in materials if m.get("is_fsc_certified", False))
        
        recycled_percent = (recycled_cost / total_material_cost) * 100.0
        fsc_percent = (fsc_wood_cost / total_material_cost) * 100.0
        
        points = 0
        if recycled_percent >= 25.0:
            points += 2
        elif recycled_percent >= 10.0:
            points += 1
            
        if fsc_percent >= 50.0:
            points += 2
        elif fsc_percent >= 25.0:
            points += 1
            
        return {
            "total_material_cost": round(total_material_cost, 2),
            "recycled_content_percent": round(recycled_percent, 1),
            "fsc_certified_wood_percent": round(fsc_percent, 1),
            "mr_credits_earned": points,
            "max_possible_points": 4,
            "compliance_status": "COMPLIANT" if points >= 2 else "NON_COMPLIANT"
        }

    @staticmethod
    def audit_indoor_air_quality(products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Audit paints, adhesives, sealants, and furniture for low-emitting VOC thresholds."""
        non_compliant_items = []
        for p in products:
            voc_g_per_l = p.get("voc_emissions_g_per_l", 0.0)
            category = p.get("category", "General")
            threshold = 50.0 if category == "Paint" else 250.0  # SCAQMD Rule 1113/1168 standard
            
            if voc_g_per_l > threshold:
                non_compliant_items.append({
                    "product_name": p.get("name"),
                    "voc_level": voc_g_per_l,
                    "threshold_limit": threshold,
                    "status": "EXCEEDS_LEED_VOC_LIMIT"
                })
                
        return {
            "total_audited_products": len(products),
            "compliant_products_count": len(products) - len(non_compliant_items),
            "non_compliant_items": non_compliant_items,
            "ieq_low_emitting_credit": len(non_compliant_items) == 0
        }

    @staticmethod
    def calculate_total_leed_score(category_scores: Dict[str, int]) -> Dict[str, Any]:
        """Calculate overall project LEED certification level (Certified, Silver, Gold, Platinum)."""
        total_points = sum(category_scores.values())
        
        certification = "Uncertified"
        if total_points >= 80:
            certification = "LEED Platinum"
        elif total_points >= 60:
            certification = "LEED Gold"
        elif total_points >= 50:
            certification = "LEED Silver"
        elif total_points >= 40:
            certification = "LEED Certified"
            
        return {
            "total_points_earned": total_points,
            "certification_tier": certification,
            "category_scores": category_scores,
            "points_to_next_tier": max(0, 40 - total_points if total_points < 40 else 50 - total_points if total_points < 50 else 60 - total_points if total_points < 60 else 80 - total_points)
        }
