"""
DreamHome Studio — Data Formatting Utilities
"""

def format_currency(amount: float, currency_symbol: str = "$") -> str:
    """Format float amount into currency string."""
    return f"{currency_symbol}{amount:,.2f}"

def format_dimensions(width_cm: float, depth_cm: float, height_cm: float) -> str:
    """Format dimensions string."""
    return f"{width_cm:.0f} W × {depth_cm:.0f} D × {height_cm:.0f} H cm"
