"""
DreamHome Studio — Budget & Cost Model
Handles project budget allocations, itemized cost line items, taxes, margins, and labor.
"""

from typing import Optional, List, Dict, Any
from database.db_manager import get_db

class BudgetLineItem:
    """Line item entity model for budgets."""

    def __init__(
        self,
        id: Optional[int] = None,
        budget_id: int = 0,
        item_name: str = "",
        category: str = "Furniture",
        item_type: str = "Furniture",
        unit_price: float = 0.0,
        quantity: int = 1,
        total_price: float = 0.0,
        supplier_id: Optional[int] = None,
        status: str = "Estimated",
        created_at: Optional[str] = None
    ):
        self.id = id
        self.budget_id = budget_id
        self.item_name = item_name
        self.category = category
        self.item_type = item_type
        self.unit_price = float(unit_price)
        self.quantity = int(quantity)
        self.total_price = float(total_price) if total_price > 0 else round(self.unit_price * self.quantity, 2)
        self.supplier_id = supplier_id
        self.status = status
        self.created_at = created_at

    def to_dict(self) -> Dict[str, Any]:
        """Serialize budget line item."""
        return {
            "id": self.id,
            "budget_id": self.budget_id,
            "item_name": self.item_name,
            "category": self.category,
            "item_type": self.item_type,
            "unit_price": self.unit_price,
            "quantity": self.quantity,
            "total_price": self.total_price,
            "supplier_id": self.supplier_id,
            "status": self.status,
            "created_at": str(self.created_at) if self.created_at else None
        }

class Budget:
    """Project budget model."""

    def __init__(
        self,
        id: Optional[int] = None,
        project_id: int = 0,
        total_estimated: float = 0.0,
        total_spent: float = 0.0,
        tax_rate: float = 0.085,
        labor_cost: float = 0.0,
        designer_margin: float = 0.15,
        notes: Optional[str] = None,
        status: str = "Draft",
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        line_items: Optional[List[BudgetLineItem]] = None
    ):
        self.id = id
        self.project_id = project_id
        self.total_estimated = float(total_estimated)
        self.total_spent = float(total_spent)
        self.tax_rate = float(tax_rate)
        self.labor_cost = float(labor_cost)
        self.designer_margin = float(designer_margin)
        self.notes = notes
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.line_items = line_items or []

    def to_dict(self) -> Dict[str, Any]:
        """Serialize budget model."""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "total_estimated": self.total_estimated,
            "total_spent": self.total_spent,
            "tax_rate": self.tax_rate,
            "labor_cost": self.labor_cost,
            "designer_margin": self.designer_margin,
            "notes": self.notes,
            "status": self.status,
            "created_at": str(self.created_at) if self.created_at else None,
            "updated_at": str(self.updated_at) if self.updated_at else None,
            "line_items": [item.to_dict() for item in self.line_items]
        }

    @classmethod
    def from_row(cls, row: Dict[str, Any], include_items: bool = True) -> "Budget":
        """Construct Budget model from row."""
        b = cls(
            id=row["id"],
            project_id=row["project_id"],
            total_estimated=row.get("total_estimated", 0.0),
            total_spent=row.get("total_spent", 0.0),
            tax_rate=row.get("tax_rate", 0.085),
            labor_cost=row.get("labor_cost", 0.0),
            designer_margin=row.get("designer_margin", 0.15),
            notes=row.get("notes"),
            status=row.get("status", "Draft"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at")
        )
        if include_items and b.id:
            b.line_items = cls.get_line_items(b.id)
        return b

    @classmethod
    def get_by_project_id(cls, project_id: int) -> Optional["Budget"]:
        """Retrieve budget for a project."""
        row = get_db().query_one("SELECT * FROM budgets WHERE project_id = ?;", (project_id,))
        return cls.from_row(row) if row else None

    @classmethod
    def get_line_items(cls, budget_id: int) -> List[BudgetLineItem]:
        """Retrieve line items for a budget."""
        rows = get_db().query_all(
            "SELECT * FROM budget_line_items WHERE budget_id = ? ORDER BY id ASC;",
            (budget_id,)
        )
        return [
            BudgetLineItem(
                id=r["id"],
                budget_id=r["budget_id"],
                item_name=r["item_name"],
                category=r["category"],
                item_type=r["item_type"],
                unit_price=r["unit_price"],
                quantity=r["quantity"],
                total_price=r["total_price"],
                supplier_id=r.get("supplier_id"),
                status=r.get("status", "Estimated"),
                created_at=r.get("created_at")
            ) for r in rows
        ]

    def recalculate_totals(self) -> "Budget":
        """Recalculate total_estimated and total_spent based on line items, labor, tax, and margins."""
        db = get_db()
        items = self.get_line_items(self.id)
        subtotal = sum(item.total_price for item in items)
        spent = sum(item.total_price for item in items if item.status in ("Purchased", "Ordered"))
        
        subtotal_with_labor = subtotal + self.labor_cost
        tax_amount = subtotal_with_labor * self.tax_rate
        margin_amount = subtotal_with_labor * self.designer_margin
        
        self.total_estimated = round(subtotal_with_labor + tax_amount + margin_amount, 2)
        self.total_spent = round(spent, 2)
        
        db.execute(
            "UPDATE budgets SET total_estimated = ?, total_spent = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?;",
            (self.total_estimated, self.total_spent, self.id)
        )
        return self
