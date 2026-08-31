"""
DreamHome Studio — Furniture Catalog Model
Handles furniture catalog items, dimensions, pricing, brand info, and catalog searches.
"""

import json
from typing import Optional, List, Dict, Any
from database.db_manager import get_db

class FurnitureCatalog:
    """Furniture item model."""

    def __init__(
        self,
        id: Optional[int] = None,
        name: str = "",
        category: str = "Living Room",
        subcategory: Optional[str] = None,
        sku: str = "",
        brand: Optional[str] = None,
        width_cm: float = 100.0,
        depth_cm: float = 80.0,
        height_cm: float = 85.0,
        price: float = 0.0,
        color_options_json: Optional[str] = None,
        material: Optional[str] = None,
        texture_url: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        default_z_index: int = 1,
        is_customizable: bool = True,
        created_at: Optional[str] = None
    ):
        self.id = id
        self.name = name
        self.category = category
        self.subcategory = subcategory
        self.sku = sku
        self.brand = brand
        self.width_cm = float(width_cm)
        self.depth_cm = float(depth_cm)
        self.height_cm = float(height_cm)
        self.price = float(price)
        self.color_options_json = color_options_json or '["#FFFFFF"]'
        self.material = material
        self.texture_url = texture_url
        self.thumbnail_url = thumbnail_url or "/static/images/catalog/default.svg"
        self.default_z_index = int(default_z_index)
        self.is_customizable = is_customizable
        self.created_at = created_at

    def to_dict(self) -> Dict[str, Any]:
        """Serialize furniture model to dictionary."""
        colors = []
        try:
            colors = json.loads(self.color_options_json) if self.color_options_json else []
        except Exception:
            colors = []

        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "subcategory": self.subcategory,
            "sku": self.sku,
            "brand": self.brand,
            "width_cm": self.width_cm,
            "depth_cm": self.depth_cm,
            "height_cm": self.height_cm,
            "price": self.price,
            "color_options": colors,
            "material": self.material,
            "texture_url": self.texture_url,
            "thumbnail_url": self.thumbnail_url,
            "default_z_index": self.default_z_index,
            "is_customizable": bool(self.is_customizable),
            "created_at": str(self.created_at) if self.created_at else None
        }

    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> "FurnitureCatalog":
        """Construct Furniture model from database row."""
        return cls(
            id=row["id"],
            name=row["name"],
            category=row["category"],
            subcategory=row.get("subcategory"),
            sku=row["sku"],
            brand=row.get("brand"),
            width_cm=row.get("width_cm", 100.0),
            depth_cm=row.get("depth_cm", 80.0),
            height_cm=row.get("height_cm", 85.0),
            price=row.get("price", 0.0),
            color_options_json=row.get("color_options_json"),
            material=row.get("material"),
            texture_url=row.get("texture_url"),
            thumbnail_url=row.get("thumbnail_url"),
            default_z_index=row.get("default_z_index", 1),
            is_customizable=bool(row.get("is_customizable", 1)),
            created_at=row.get("created_at")
        )

    @classmethod
    def get_by_id(cls, item_id: int) -> Optional["FurnitureCatalog"]:
        """Retrieve furniture item by ID."""
        row = get_db().query_one("SELECT * FROM furniture_catalog WHERE id = ?;", (item_id,))
        return cls.from_row(row) if row else None

    @classmethod
    def get_all(
        cls,
        category: Optional[str] = None,
        search_query: Optional[str] = None,
        max_price: Optional[float] = None
    ) -> List["FurnitureCatalog"]:
        """Search and filter furniture catalog."""
        query = "SELECT * FROM furniture_catalog WHERE 1=1"
        params = []

        if category and category.lower() != "all":
            query += " AND LOWER(category) = LOWER(?)"
            params.append(category)

        if search_query:
            query += " AND (LOWER(name) LIKE ? OR LOWER(brand) LIKE ? OR LOWER(sku) LIKE ?)"
            term = f"%{search_query.lower()}%"
            params.extend([term, term, term])

        if max_price:
            query += " AND price <= ?"
            params.append(max_price)

        query += " ORDER BY category ASC, name ASC;"
        rows = get_db().query_all(query, tuple(params))
        return [cls.from_row(r) for r in rows]

    @classmethod
    def create(cls, **kwargs) -> "FurnitureCatalog":
        """Create new catalog item."""
        colors = kwargs.get("color_options", ["#FFFFFF"])
        colors_json = json.dumps(colors) if isinstance(colors, list) else str(colors)
        
        db = get_db()
        item_id = db.execute(
            """INSERT INTO furniture_catalog 
               (name, category, subcategory, sku, brand, width_cm, depth_cm, height_cm, price, color_options_json, material, texture_url, thumbnail_url, default_z_index, is_customizable) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
            (
                kwargs["name"], kwargs["category"], kwargs.get("subcategory"),
                kwargs["sku"], kwargs.get("brand"), kwargs.get("width_cm", 100.0),
                kwargs.get("depth_cm", 80.0), kwargs.get("height_cm", 85.0),
                kwargs.get("price", 0.0), colors_json, kwargs.get("material"),
                kwargs.get("texture_url"), kwargs.get("thumbnail_url"),
                kwargs.get("default_z_index", 1), kwargs.get("is_customizable", 1)
            )
        )
        return cls.get_by_id(item_id)
