"""
DreamHome Studio — Supply Chain & ERP Procurement Service
Predicts supplier lead times, reorder points, shipment tracking,
warehouse bin location mapping, and volume discount matrices.
"""

from typing import List, Dict, Any

class SupplyChainProcurementERP:
    """Enterprise procurement supply chain management engine."""

    @staticmethod
    def calculate_reorder_point(daily_demand: float, lead_time_days: int, safety_stock: int = 5) -> int:
        """Calculate inventory reorder point based on lead time demand and safety stock."""
        lead_time_demand = daily_demand * lead_time_days
        reorder_point = math.ceil(lead_time_demand + safety_stock)
        return reorder_point

    @staticmethod
    def calculate_volume_discount(unit_price: float, quantity: int) -> Dict[str, Any]:
        """Apply tier volume discount matrix to bulk furniture orders."""
        discount_percent = 0.0
        if quantity >= 100:
            discount_percent = 25.0
        elif quantity >= 50:
            discount_percent = 18.0
        elif quantity >= 20:
            discount_percent = 12.0
        elif quantity >= 10:
            discount_percent = 5.0
            
        gross_total = unit_price * quantity
        discount_amount = gross_total * (discount_percent / 100.0)
        net_total = gross_total - discount_amount
        
        return {
            "quantity": quantity,
            "unit_price": unit_price,
            "gross_total": round(gross_total, 2),
            "discount_percent": discount_percent,
            "discount_amount": round(discount_amount, 2),
            "net_total": round(net_total, 2),
            "savings": round(discount_amount, 2)
        }

    @staticmethod
    def assign_warehouse_bin_locations(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Map inventory items to warehouse rack, aisle, and bin coordinates."""
        mapped = []
        for i, item in enumerate(items):
            aisle = chr(65 + (i % 8))  # Aisles A-H
            rack = (i // 8) % 20 + 1   # Racks 1-20
            bin_num = (i % 4) + 1      # Bins 1-4
            
            bin_code = f"W1-{aisle}{rack:02d}-B{bin_num}"
            
            item_copy = item.copy()
            item_copy["bin_location"] = bin_code
            mapped.append(item_copy)
        return mapped
