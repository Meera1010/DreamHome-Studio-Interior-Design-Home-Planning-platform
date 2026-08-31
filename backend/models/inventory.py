"""
DreamHome Studio — Inventory Data Model
Tracks warehouse furniture stock levels, reorder thresholds, unit costs, and supplier links.
"""

from typing import Optional, List, Dict, Any
from database.db_manager import get_db

class InventoryItem:
    """Inventory item entity model."""

    def __init__(
        self,
        id: Optional[int] = None,
        furniture_id: int = 0,
        supplier_id: int = 0,
        quantity_in_stock: int = 0,
        reorder_level: int = 5,
        unit_cost: float = 0.0,
        bin_location: Optional[str] = None,
        status: str = "In Stock",
        last_restocked_at: Optional[str] = None,
        furniture_name: Optional[str] = None,
        supplier_name: Optional[str] = None,
        sku: Optional[str] = None
    ):
        self.id = id
        self.furniture_id = furniture_id
        self.supplier_id = supplier_id
        self.quantity_in_stock = int(quantity_in_stock)
        self.reorder_level = int(reorder_level)
        self.unit_cost = float(unit_cost)
        self.bin_location = bin_location
        self.status = status
        self.last_restocked_at = last_restocked_at
        self.furniture_name = furniture_name
        self.supplier_name = supplier_name
        self.sku = sku

    def to_dict(self) -> Dict[str, Any]:
        """Serialize inventory model to dictionary."""
        return {
            "id": self.id,
            "furniture_id": self.furniture_id,
            "supplier_id": self.supplier_id,
            "quantity_in_stock": self.quantity_in_stock,
            "reorder_level": self.reorder_level,
            "unit_cost": self.unit_cost,
            "bin_location": self.bin_location,
            "status": self.status,
            "last_restocked_at": str(self.last_restocked_at) if self.last_restocked_at else None,
            "furniture_name": self.furniture_name,
            "supplier_name": self.supplier_name,
            "sku": self.sku
        }

    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> "InventoryItem":
        """Construct InventoryItem model from database row."""
        return cls(
            id=row["id"],
            furniture_id=row["furniture_id"],
            supplier_id=row["supplier_id"],
            quantity_in_stock=row.get("quantity_in_stock", 0),
            reorder_level=row.get("reorder_level", 5),
            unit_cost=row.get("unit_cost", 0.0),
            bin_location=row.get("bin_location"),
            status=row.get("status", "In Stock"),
            last_restocked_at=row.get("last_restocked_at"),
            furniture_name=row.get("furniture_name"),
            supplier_name=row.get("supplier_name"),
            sku=row.get("sku")
        )

    @classmethod
    def get_by_id(cls, item_id: int) -> Optional["InventoryItem"]:
        """Retrieve inventory item by ID."""
        query = """
            SELECT i.*, f.name as furniture_name, f.sku, s.company_name as supplier_name
            FROM inventory_items i
            JOIN furniture_catalog f ON i.furniture_id = f.id
            JOIN suppliers s ON i.supplier_id = s.id
            WHERE i.id = ?;
        """
        row = get_db().query_one(query, (item_id,))
        return cls.from_row(row) if row else None

    @classmethod
    def get_all(cls, status_filter: Optional[str] = None) -> List["InventoryItem"]:
        """Retrieve all inventory items with optional status filtering."""
        query = """
            SELECT i.*, f.name as furniture_name, f.sku, s.company_name as supplier_name
            FROM inventory_items i
            JOIN furniture_catalog f ON i.furniture_id = f.id
            JOIN suppliers s ON i.supplier_id = s.id
            WHERE 1=1
        """
        params = []
        if status_filter:
            query += " AND i.status = ?"
            params.append(status_filter)

        query += " ORDER BY i.quantity_in_stock ASC, f.name ASC;"
        rows = get_db().query_all(query, tuple(params))
        return [cls.from_row(r) for r in rows]

    @classmethod
    def create(cls, **kwargs) -> "InventoryItem":
        """Create a new warehouse inventory record."""
        db = get_db()
        item_id = db.execute(
            """INSERT INTO inventory_items 
               (furniture_id, supplier_id, quantity_in_stock, reorder_level, unit_cost, bin_location, status) 
               VALUES (?, ?, ?, ?, ?, ?, ?);""",
            (
                kwargs["furniture_id"], kwargs["supplier_id"],
                kwargs.get("quantity_in_stock", 0), kwargs.get("reorder_level", 5),
                kwargs.get("unit_cost", 0.0), kwargs.get("bin_location"),
                kwargs.get("status", "In Stock")
            )
        )
        return cls.get_by_id(item_id)
