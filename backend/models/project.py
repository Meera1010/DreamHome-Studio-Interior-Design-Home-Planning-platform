"""
DreamHome Studio — Project Data Model
Handles multi-room interior design project records, client/designer assignments,
budget limits, and status workflow transitions.
"""

from typing import Optional, List, Dict, Any
from database.db_manager import get_db

class Project:
    """Project entity model."""

    def __init__(
        self,
        id: Optional[int] = None,
        title: str = "",
        description: Optional[str] = None,
        client_id: Optional[int] = None,
        designer_id: int = 0,
        status: str = "Planning",
        budget_limit: float = 0.0,
        currency: str = "USD",
        cover_image: Optional[str] = None,
        target_completion_date: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        client_name: Optional[str] = None,
        designer_name: Optional[str] = None
    ):
        self.id = id
        self.title = title
        self.description = description
        self.client_id = client_id
        self.designer_id = designer_id
        self.status = status
        self.budget_limit = float(budget_limit)
        self.currency = currency
        self.cover_image = cover_image or "/static/images/projects/default_cover.jpg"
        self.target_completion_date = target_completion_date
        self.created_at = created_at
        self.updated_at = updated_at
        self.client_name = client_name
        self.designer_name = designer_name

    def to_dict(self) -> Dict[str, Any]:
        """Serialize project instance to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "client_id": self.client_id,
            "designer_id": self.designer_id,
            "status": self.status,
            "budget_limit": self.budget_limit,
            "currency": self.currency,
            "cover_image": self.cover_image,
            "target_completion_date": str(self.target_completion_date) if self.target_completion_date else None,
            "created_at": str(self.created_at) if self.created_at else None,
            "updated_at": str(self.updated_at) if self.updated_at else None,
            "client_name": self.client_name,
            "designer_name": self.designer_name
        }

    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> "Project":
        """Construct Project model from SQLite database row."""
        return cls(
            id=row["id"],
            title=row["title"],
            description=row.get("description"),
            client_id=row.get("client_id"),
            designer_id=row["designer_id"],
            status=row.get("status", "Planning"),
            budget_limit=row.get("budget_limit", 0.0),
            currency=row.get("currency", "USD"),
            cover_image=row.get("cover_image"),
            target_completion_date=row.get("target_completion_date"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
            client_name=row.get("client_name"),
            designer_name=row.get("designer_name")
        )

    @classmethod
    def get_by_id(cls, project_id: int) -> Optional["Project"]:
        """Retrieve project by ID with joined client and designer names."""
        query = """
            SELECT p.*, c.full_name as client_name, d.full_name as designer_name
            FROM projects p
            LEFT JOIN users c ON p.client_id = c.id
            LEFT JOIN users d ON p.designer_id = d.id
            WHERE p.id = ?;
        """
        row = get_db().query_one(query, (project_id,))
        return cls.from_row(row) if row else None

    @classmethod
    def get_all(
        cls,
        user_id: Optional[int] = None,
        role: Optional[str] = None,
        status: Optional[str] = None
    ) -> List["Project"]:
        """Retrieve projects filtered by user access role or status."""
        query = """
            SELECT p.*, c.full_name as client_name, d.full_name as designer_name
            FROM projects p
            LEFT JOIN users c ON p.client_id = c.id
            LEFT JOIN users d ON p.designer_id = d.id
            WHERE 1=1
        """
        params = []

        if user_id and role:
            if role == "Designer":
                query += " AND p.designer_id = ?"
                params.append(user_id)
            elif role == "Client":
                query += " AND p.client_id = ?"
                params.append(user_id)

        if status:
            query += " AND p.status = ?"
            params.append(status)

        query += " ORDER BY p.updated_at DESC;"
        rows = get_db().query_all(query, tuple(params))
        return [cls.from_row(r) for r in rows]

    @classmethod
    def create(
        cls,
        title: str,
        designer_id: int,
        description: Optional[str] = None,
        client_id: Optional[int] = None,
        status: str = "Planning",
        budget_limit: float = 0.0,
        currency: str = "USD",
        target_completion_date: Optional[str] = None,
        cover_image: Optional[str] = None
    ) -> "Project":
        """Create new interior design project record."""
        db = get_db()
        project_id = db.execute(
            """INSERT INTO projects 
               (title, description, client_id, designer_id, status, budget_limit, currency, target_completion_date, cover_image) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""",
            (title.strip(), description, client_id, designer_id, status, budget_limit, currency, target_completion_date, cover_image)
        )
        return cls.get_by_id(project_id)

    def update(self, **kwargs) -> "Project":
        """Update project fields."""
        allowed = {"title", "description", "client_id", "designer_id", "status", "budget_limit", "currency", "cover_image", "target_completion_date"}
        updates = []
        params = []
        for k, v in kwargs.items():
            if k in allowed:
                setattr(self, k, v)
                updates.append(f"{k} = ?")
                params.append(v)
        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            params.append(self.id)
            get_db().execute(f"UPDATE projects SET {', '.join(updates)} WHERE id = ?;", tuple(params))
        return Project.get_by_id(self.id)

    def delete(self) -> bool:
        """Delete project record."""
        return get_db().execute("DELETE FROM projects WHERE id = ?;", (self.id,)) > 0
