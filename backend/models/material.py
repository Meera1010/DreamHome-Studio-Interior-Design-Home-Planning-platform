"""
DreamHome Studio — Material Catalog Model
Handles flooring, wall paint, wallpaper, tile, fabric, and surface finish materials.
"""

from typing import Optional, List, Dict, Any
from database.db_manager import get_db

class MaterialCatalog:
    """Material catalog entity model."""

    def __init__(
        self,
        id: Optional[int] = None,
        name: str = "",
        category: str = "Flooring",
        texture_url: Optional[str] = None,
        pattern_type: str = "solid",
        color_hex: str = "#FFFFFF",
        price_per_sqm: float = 0.0,
        roughness: float = 0.5,
        opacity: float = 1.0,
        created_at: Optional[str] = None
    ):
        self.id = id
        self.name = name
        self.category = category
        self.texture_url = texture_url
        self.pattern_type = pattern_type
        self.color_hex = color_hex
        self.price_per_sqm = float(price_per_sqm)
        self.roughness = float(roughness)
        self.opacity = float(opacity)
        self.created_at = created_at

    def to_dict(self) -> Dict[str, Any]:
        """Serialize material model."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "texture_url": self.texture_url,
            "pattern_type": self.pattern_type,
            "color_hex": self.color_hex,
            "price_per_sqm": self.price_per_sqm,
            "roughness": self.roughness,
            "opacity": self.opacity,
            "created_at": str(self.created_at) if self.created_at else None
        }

    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> "MaterialCatalog":
        """Construct material model from SQLite row."""
        return cls(
            id=row["id"],
            name=row["name"],
            category=row["category"],
            texture_url=row.get("texture_url"),
            pattern_type=row.get("pattern_type", "solid"),
            color_hex=row.get("color_hex", "#FFFFFF"),
            price_per_sqm=row.get("price_per_sqm", 0.0),
            roughness=row.get("roughness", 0.5),
            opacity=row.get("opacity", 1.0),
            created_at=row.get("created_at")
        )

    @classmethod
    def get_by_id(cls, item_id: int) -> Optional["MaterialCatalog"]:
        """Retrieve material by ID."""
        row = get_db().query_one("SELECT * FROM materials_catalog WHERE id = ?;", (item_id,))
        return cls.from_row(row) if row else None

    @classmethod
    def get_all(cls, category: Optional[str] = None) -> List["MaterialCatalog"]:
        """Retrieve all materials with optional category filter."""
        query = "SELECT * FROM materials_catalog WHERE 1=1"
        params = []
        if category and category.lower() != "all":
            query += " AND LOWER(category) = LOWER(?)"
            params.append(category)
        query += " ORDER BY category ASC, name ASC;"
        rows = get_db().query_all(query, tuple(params))
        return [cls.from_row(r) for r in rows]
