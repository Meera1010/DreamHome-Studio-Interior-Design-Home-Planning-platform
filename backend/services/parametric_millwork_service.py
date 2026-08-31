"""
DreamHome Studio — Parametric Millwork & Joinery Service
Generates 2D elevation cut lists, board-feet lumber estimates,
and custom cabinetry dimensions.
"""

from typing import List, Dict, Any

class ParametricMillworkService:
    """Service for custom cabinetry and architectural millwork planning."""

    @staticmethod
    def calculate_lumber_board_feet(width_cm: float, depth_cm: float, height_cm: float, thickness_cm: float = 1.9) -> Dict[str, Any]:
        """Compute board-feet lumber required for custom cabinet carcass."""
        # Convert cm to inches
        w_in = width_cm / 2.54
        d_in = depth_cm / 2.54
        h_in = height_cm / 2.54
        t_in = thickness_cm / 2.54
        
        # Estimate surface area of 4 sides + back + 2 shelves
        sides_sq_in = 2 * (d_in * h_in)
        top_bottom_sq_in = 2 * (w_in * d_in)
        back_sq_in = w_in * h_in
        shelves_sq_in = 2 * (w_in * d_in)
        
        total_sq_in = sides_sq_in + top_bottom_sq_in + back_sq_in + shelves_sq_in
        board_feet = (total_sq_in * t_in) / 144.0
        
        # Add 15% waste factor for milling
        board_feet_with_waste = board_feet * 1.15
        
        return {
            "cabinet_dimensions_cm": {"width": width_cm, "depth": depth_cm, "height": height_cm},
            "net_board_feet": round(board_feet, 2),
            "gross_board_feet_with_waste": round(board_feet_with_waste, 2),
            "recommended_plywood_sheets_4x8": max(1, round(total_sq_in / (48 * 96), 1))
        }

    @staticmethod
    def generate_cut_list(width_cm: float, depth_cm: float, height_cm: float) -> List[Dict[str, Any]]:
        """Generate itemized wood cut list for cabinet fabrication."""
        return [
            {"part": "Side Panels (x2)", "width_cm": depth_cm, "length_cm": height_cm, "material": "3/4 inch Hardwood Plywood"},
            {"part": "Top & Bottom Plates (x2)", "width_cm": depth_cm, "length_cm": width_cm - 3.8, "material": "3/4 inch Hardwood Plywood"},
            {"part": "Backing Panel (x1)", "width_cm": width_cm, "length_cm": height_cm, "material": "1/4 inch Plywood"},
            {"part": "Adjustable Shelves (x2)", "width_cm": depth_cm - 2.0, "length_cm": width_cm - 4.0, "material": "3/4 inch Hardwood Plywood"}
        ]
