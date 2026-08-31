"""
DreamHome Studio — Inventory Procurement & Supply Chain Service
Calculates economic order quantities (EOQ), supplier performance index,
and safety stock thresholds for warehouse inventory management.
"""

import math
from typing import Dict, Any, List
from backend.models.inventory import InventoryItem
from backend.models.supplier import Supplier

class InventoryProcurementService:
    """Supply chain forecasting and warehouse procurement engine."""

    @classmethod
    def calculate_eoq(
        cls,
        annual_demand: float,
        order_cost: float = 50.0,
        holding_cost_rate: float = 0.15,
        unit_cost: float = 100.0
    ) -> Dict[str, Any]:
        """
        Calculate Economic Order Quantity (EOQ):
        EOQ = sqrt((2 * Demand * OrderCost) / HoldingCost)
        """
        holding_cost = unit_cost * holding_cost_rate
        if holding_cost <= 0 or annual_demand <= 0:
            return {"eoq": 1, "annual_orders": 1}

        eoq = math.sqrt((2 * annual_demand * order_cost) / holding_cost)
        eoq_rounded = max(1, int(round(eoq)))
        annual_orders = round(annual_demand / eoq_rounded, 1)

        return {
            "annual_demand": annual_demand,
            "order_cost": order_cost,
            "unit_cost": unit_cost,
            "holding_cost_unit": round(holding_cost, 2),
            "eoq": eoq_rounded,
            "annual_orders": annual_orders
        }

    @classmethod
    def audit_supplier_performance(cls) -> List[Dict[str, Any]]:
        """Compute performance index score (0-100) for all suppliers."""
        suppliers = Supplier.get_all()
        results = []
        for s in suppliers:
            # Score formula based on rating and lead time
            lead_score = max(0.0, 50.0 - (s.lead_time_days * 2.5))
            rating_score = (s.rating / 5.0) * 50.0
            total_score = round(lead_score + rating_score, 1)

            results.append({
                "supplier_id": s.id,
                "supplier_name": s.name,
                "rating": s.rating,
                "lead_time_days": s.lead_time_days,
                "performance_score": total_score,
                "status": "Preferred" if total_score >= 80 else "Standard" if total_score >= 60 else "Under Review"
            })
        return results
