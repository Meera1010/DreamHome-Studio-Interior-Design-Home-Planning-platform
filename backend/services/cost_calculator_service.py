"""
DreamHome Studio — Interior Cost Calculator Service
Computes detailed cost breakdowns based on 2D floorplan items, furniture pricing,
wall surface paint areas, flooring cost per sqm, labor costs, sales taxes, and designer margins.
"""

from typing import Dict, Any, List, Optional
from backend.models.furniture import FurnitureCatalog
from backend.models.material import MaterialCatalog
from config import Config

class CostCalculatorService:
    """Interior design cost calculation service."""

    @staticmethod
    def calculate_floorplan_costs(
        canvas_data: Dict[str, Any],
        flooring_material_id: Optional[int] = None,
        wall_material_id: Optional[int] = None,
        custom_labor_rate: Optional[float] = None,
        tax_rate: float = Config.DEFAULT_TAX_RATE,
        designer_margin: float = Config.DEFAULT_DESIGNER_MARGIN
    ) -> Dict[str, Any]:
        """
        Dynamically calculate itemized costs for a floorplan layout.
        """
        objects = canvas_data.get("objects", [])
        walls = canvas_data.get("walls", [])
        room = canvas_data.get("room", {})
        
        scale = float(canvas_data.get("scale_factor", 50.0))  # 50px = 1m
        width_m = float(room.get("width_m", 8.0))
        height_m = float(room.get("height_m", 6.0))
        floor_area_sqm = width_m * height_m

        # 1. Furniture Cost Breakdown
        furniture_line_items = []
        furniture_subtotal = 0.0

        for obj in objects:
            cat_id = obj.get("catalog_id")
            item_name = obj.get("name", "Custom Item")
            price = float(obj.get("price", 0.0))
            
            if cat_id:
                catalog_item = FurnitureCatalog.get_by_id(cat_id)
                if catalog_item:
                    price = catalog_item.price
                    item_name = catalog_item.name
                    
            furniture_line_items.append({
                "item_name": item_name,
                "category": obj.get("category", "Furniture"),
                "unit_price": price,
                "quantity": 1,
                "total_price": price
            })
            furniture_subtotal += price

        # 2. Flooring & Wall Surface Material Costs
        flooring_cost = 0.0
        flooring_name = "Standard Flooring"
        if flooring_material_id:
            mat = MaterialCatalog.get_by_id(flooring_material_id)
            if mat:
                flooring_cost = round(mat.price_per_sqm * floor_area_sqm, 2)
                flooring_name = mat.name
        else:
            flooring_cost = round(85.0 * floor_area_sqm, 2)  # Default $85/sqm

        # Wall surface area estimation (assume 2.8m wall height)
        wall_height_m = 2.8
        total_wall_length_m = 0.0
        for w in walls:
            dx = float(w.get("x2", 0)) - float(w.get("x1", 0))
            dy = float(w.get("y2", 0)) - float(w.get("y1", 0))
            dist_m = (dx**2 + dy**2)**0.5 / scale
            total_wall_length_m += dist_m

        if total_wall_length_m == 0.0:
            total_wall_length_m = (width_m + height_m) * 2.0

        wall_surface_sqm = total_wall_length_m * wall_height_m
        wall_paint_cost = 0.0
        wall_paint_name = "Standard Paint"
        if wall_material_id:
            mat = MaterialCatalog.get_by_id(wall_material_id)
            if mat:
                wall_paint_cost = round(mat.price_per_sqm * wall_surface_sqm, 2)
                wall_paint_name = mat.name
        else:
            wall_paint_cost = round(35.0 * wall_surface_sqm, 2)  # Default $35/sqm

        materials_subtotal = round(flooring_cost + wall_paint_cost, 2)

        # 3. Labor Costs
        labor_rate_sqm = custom_labor_rate if custom_labor_rate is not None else Config.DEFAULT_LABOR_RATE_PER_SQM
        labor_subtotal = round(floor_area_sqm * labor_rate_sqm, 2)

        # 4. Tax & Designer Margin
        subtotal_before_tax = furniture_subtotal + materials_subtotal + labor_subtotal
        tax_amount = round(subtotal_before_tax * tax_rate, 2)
        margin_amount = round(subtotal_before_tax * designer_margin, 2)
        grand_total = round(subtotal_before_tax + tax_amount + margin_amount, 2)

        return {
            "summary": {
                "floor_area_sqm": round(floor_area_sqm, 2),
                "wall_surface_sqm": round(wall_surface_sqm, 2),
                "furniture_count": len(furniture_line_items),
                "furniture_subtotal": round(furniture_subtotal, 2),
                "materials_subtotal": materials_subtotal,
                "labor_subtotal": labor_subtotal,
                "subtotal_before_tax": round(subtotal_before_tax, 2),
                "tax_rate": tax_rate,
                "tax_amount": tax_amount,
                "designer_margin": designer_margin,
                "margin_amount": margin_amount,
                "grand_total": grand_total
            },
            "flooring": {
                "name": flooring_name,
                "area_sqm": round(floor_area_sqm, 2),
                "cost": flooring_cost
            },
            "wall_finish": {
                "name": wall_paint_name,
                "surface_sqm": round(wall_surface_sqm, 2),
                "cost": wall_paint_cost
            },
            "furniture_items": furniture_line_items
        }
