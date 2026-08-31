"""
DreamHome Studio — Input Validation Utilities
Validates API JSON payloads, data types, and mandatory fields.
"""

from typing import Dict, Any, List, Tuple, Optional

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> Tuple[bool, Optional[str]]:
    """Verify that all required keys exist and are non-empty in input dictionary."""
    if not isinstance(data, dict):
        return False, "Invalid JSON payload"
        
    missing = [field for field in required_fields if field not in data or data[field] is None or (isinstance(data[field], str) and not data[field].strip())]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
        
    return True, None
