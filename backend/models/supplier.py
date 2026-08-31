"""
DreamHome Studio — Supplier Data Model
Manages furniture manufacturers, fabric suppliers, ratings, lead times, and contact information.
"""

from typing import Optional, List, Dict, Any
from database.db_manager import get_db

class Supplier:
    """Supplier entity model."""

    def __init__(
        self,
        id: Optional[int] = None,
        company_name: str = "",
        contact_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        website: Optional[str] = None,
        address: Optional[str] = None,
        rating: float = 4.5,
        lead_time_days: int = 7,
        notes: Optional[str] = None,
        created_at: Optional[str] = None
    ):
        self.id = id
        self.company_name = company_name
        self.contact_name = contact_name
        self.email = email
        self.phone = phone
        self.website = website
        self.address = address
        self.rating = float(rating)
        self.lead_time_days = int(lead_time_days)
        self.notes = notes
        self.created_at = created_at

    def to_dict(self) -> Dict[str, Any]:
        """Serialize supplier record."""
        return {
            "id": self.id,
            "company_name": self.company_name,
            "contact_name": self.contact_name,
            "email": self.email,
            "phone": self.phone,
            "website": self.website,
            "address": self.address,
            "rating": self.rating,
            "lead_time_days": self.lead_time_days,
            "notes": self.notes,
            "created_at": str(self.created_at) if self.created_at else None
        }

    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> "Supplier":
        """Construct Supplier model from row."""
        return cls(
            id=row["id"],
            company_name=row["company_name"],
            contact_name=row.get("contact_name"),
            email=row.get("email"),
            phone=row.get("phone"),
            website=row.get("website"),
            address=row.get("address"),
            rating=row.get("rating", 4.5),
            lead_time_days=row.get("lead_time_days", 7),
            notes=row.get("notes"),
            created_at=row.get("created_at")
        )

    @classmethod
    def get_by_id(cls, supplier_id: int) -> Optional["Supplier"]:
        """Retrieve supplier by ID."""
        row = get_db().query_one("SELECT * FROM suppliers WHERE id = ?;", (supplier_id,))
        return cls.from_row(row) if row else None

    @classmethod
    def get_all(cls) -> List["Supplier"]:
        """Retrieve all suppliers."""
        rows = get_db().query_all("SELECT * FROM suppliers ORDER BY rating DESC, company_name ASC;")
        return [cls.from_row(r) for r in rows]

    @classmethod
    def create(cls, **kwargs) -> "Supplier":
        """Create new supplier record."""
        db = get_db()
        sup_id = db.execute(
            """INSERT INTO suppliers 
               (company_name, contact_name, email, phone, website, address, rating, lead_time_days, notes) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""",
            (
                kwargs["company_name"], kwargs.get("contact_name"), kwargs.get("email"),
                kwargs.get("phone"), kwargs.get("website"), kwargs.get("address"),
                kwargs.get("rating", 4.5), kwargs.get("lead_time_days", 7), kwargs.get("notes")
            )
        )
        return cls.get_by_id(sup_id)
