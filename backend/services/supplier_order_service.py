"""
DreamHome Studio — Supplier Order & Inventory Restocking Service
Generates purchase orders, manages warehouse inventory reorders, tracks lead-time dates,
and computes supplier reliability metrics.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from database.db_manager import get_db
from backend.models.supplier import Supplier
from backend.models.inventory import InventoryItem

class SupplierOrderService:
    """Supplier purchase order and automated inventory restocking engine."""

    @classmethod
    def audit_low_stock_items(cls) -> List[Dict[str, Any]]:
        """Identify all warehouse inventory items below reorder threshold."""
        items = InventoryItem.get_all()
        reorder_list = []
        for item in items:
            if item.quantity_in_stock <= item.reorder_level:
                supplier = Supplier.get_by_id(item.supplier_id)
                lead_days = supplier.lead_time_days if supplier else 7
                est_delivery = datetime.now() + timedelta(days=lead_days)

                reorder_list.append({
                    "inventory_id": item.id,
                    "furniture_name": item.furniture_name,
                    "sku": item.sku,
                    "current_stock": item.quantity_in_stock,
                    "reorder_level": item.reorder_level,
                    "suggested_reorder_qty": (item.reorder_level * 3) - item.quantity_in_stock,
                    "unit_cost": item.unit_cost,
                    "supplier_id": item.supplier_id,
                    "supplier_name": item.supplier_name,
                    "lead_time_days": lead_days,
                    "estimated_delivery_date": est_delivery.strftime("%Y-%m-%d")
                })
        return reorder_list

    @classmethod
    def generate_purchase_order(
        cls,
        supplier_id: int,
        item_orders: List[Dict[str, Any]],
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate formal purchase order payload for a supplier.
        """
        supplier = Supplier.get_by_id(supplier_id)
        if not supplier:
            return {"error": "Supplier not found"}

        order_lines = []
        total_order_cost = 0.0

        for order in item_orders:
            inv_id = order.get("inventory_id")
            qty = int(order.get("quantity", 1))
            unit_cost = float(order.get("unit_cost", 0.0))
            line_total = round(unit_cost * qty, 2)

            order_lines.append({
                "inventory_id": inv_id,
                "item_name": order.get("furniture_name", "Catalog Item"),
                "sku": order.get("sku"),
                "quantity": qty,
                "unit_cost": unit_cost,
                "total_cost": line_total
            })
            total_order_cost += line_total

        po_number = f"PO-{datetime.now().strftime('%Y%m%d')}-{supplier_id:03d}"
        est_delivery = datetime.now() + timedelta(days=supplier.lead_time_days)

        return {
            "po_number": po_number,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "supplier": supplier.to_dict(),
            "items": order_lines,
            "total_order_cost": round(total_order_cost, 2),
            "estimated_delivery_date": est_delivery.strftime("%Y-%m-%d"),
            "notes": notes or "Automated restock purchase order"
        }
