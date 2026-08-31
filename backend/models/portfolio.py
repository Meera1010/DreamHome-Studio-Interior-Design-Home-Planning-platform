"""
DreamHome Studio — Portfolio & Showcase Model
Handles designer project showcases, public gallery items, likes, and view counts.
"""

from typing import Optional, List, Dict, Any
from database.db_manager import get_db

class Portfolio:
    """Designer Portfolio entity model."""

    def __init__(
        self,
        id: Optional[int] = None,
        designer_id: int = 0,
        project_id: Optional[int] = None,
        title: str = "",
        description: Optional[str] = None,
        cover_image: Optional[str] = None,
        tags: Optional[str] = None,
        view_count: int = 0,
        like_count: int = 0,
        is_public: bool = True,
        created_at: Optional[str] = None,
        designer_name: Optional[str] = None,
        designer_avatar: Optional[str] = None
    ):
        self.id = id
        self.designer_id = designer_id
        self.project_id = project_id
        self.title = title
        self.description = description
        self.cover_image = cover_image or "/static/images/portfolio/default.jpg"
        self.tags = tags
        self.view_count = int(view_count)
        self.like_count = int(like_count)
        self.is_public = is_public
        self.created_at = created_at
        self.designer_name = designer_name
        self.designer_avatar = designer_avatar

    def to_dict(self) -> Dict[str, Any]:
        """Serialize portfolio item."""
        return {
            "id": self.id,
            "designer_id": self.designer_id,
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "cover_image": self.cover_image,
            "tags": self.tags,
            "view_count": self.view_count,
            "like_count": self.like_count,
            "is_public": bool(self.is_public),
            "created_at": str(self.created_at) if self.created_at else None,
            "designer_name": self.designer_name,
            "designer_avatar": self.designer_avatar
        }

    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> "Portfolio":
        """Construct Portfolio model from database row."""
        return cls(
            id=row["id"],
            designer_id=row["designer_id"],
            project_id=row.get("project_id"),
            title=row["title"],
            description=row.get("description"),
            cover_image=row.get("cover_image"),
            tags=row.get("tags"),
            view_count=row.get("view_count", 0),
            like_count=row.get("like_count", 0),
            is_public=bool(row.get("is_public", 1)),
            created_at=row.get("created_at"),
            designer_name=row.get("designer_name"),
            designer_avatar=row.get("designer_avatar")
        )

    @classmethod
    def get_public_showcases(cls) -> List["Portfolio"]:
        """Retrieve public portfolio showcases."""
        query = """
            SELECT p.*, u.full_name as designer_name, u.avatar_url as designer_avatar 
            FROM portfolios p 
            JOIN users u ON p.designer_id = u.id 
            WHERE p.is_public = 1 
            ORDER BY p.like_count DESC, p.created_at DESC;
        """
        rows = get_db().query_all(query)
        return [cls.from_row(r) for r in rows]

    @classmethod
    def create(cls, **kwargs) -> "Portfolio":
        """Create new portfolio item."""
        db = get_db()
        p_id = db.execute(
            """INSERT INTO portfolios 
               (designer_id, project_id, title, description, cover_image, tags, is_public) 
               VALUES (?, ?, ?, ?, ?, ?, ?);""",
            (
                kwargs["designer_id"], kwargs.get("project_id"), kwargs["title"].strip(),
                kwargs.get("description"), kwargs.get("cover_image"), kwargs.get("tags"),
                kwargs.get("is_public", 1)
            )
        )
        row = db.query_one(
            """SELECT p.*, u.full_name as designer_name, u.avatar_url as designer_avatar 
               FROM portfolios p JOIN users u ON p.designer_id = u.id WHERE p.id = ?;""",
            (p_id,)
        )
        return cls.from_row(row)
