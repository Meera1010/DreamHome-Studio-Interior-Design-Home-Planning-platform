"""
DreamHome Studio — Comment & Feedback Model
Handles client/designer floorplan feedback pins, comments, and resolution workflows.
"""

from typing import Optional, List, Dict, Any
from database.db_manager import get_db

class Comment:
    """Comment & visual pin annotation model."""

    def __init__(
        self,
        id: Optional[int] = None,
        project_id: int = 0,
        floorplan_id: Optional[int] = None,
        user_id: int = 0,
        pos_x: Optional[float] = None,
        pos_y: Optional[float] = None,
        comment_text: str = "",
        status: str = "Open",
        parent_id: Optional[int] = None,
        created_at: Optional[str] = None,
        user_name: Optional[str] = None,
        user_avatar: Optional[str] = None,
        user_role: Optional[str] = None
    ):
        self.id = id
        self.project_id = project_id
        self.floorplan_id = floorplan_id
        self.user_id = user_id
        self.pos_x = float(pos_x) if pos_x is not None else None
        self.pos_y = float(pos_y) if pos_y is not None else None
        self.comment_text = comment_text
        self.status = status
        self.parent_id = parent_id
        self.created_at = created_at
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.user_role = user_role

    def to_dict(self) -> Dict[str, Any]:
        """Serialize comment model."""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "floorplan_id": self.floorplan_id,
            "user_id": self.user_id,
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
            "comment_text": self.comment_text,
            "status": self.status,
            "parent_id": self.parent_id,
            "created_at": str(self.created_at) if self.created_at else None,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "user_role": self.user_role
        }

    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> "Comment":
        """Construct Comment model from database row."""
        return cls(
            id=row["id"],
            project_id=row["project_id"],
            floorplan_id=row.get("floorplan_id"),
            user_id=row["user_id"],
            pos_x=row.get("pos_x"),
            pos_y=row.get("pos_y"),
            comment_text=row["comment_text"],
            status=row.get("status", "Open"),
            parent_id=row.get("parent_id"),
            created_at=row.get("created_at"),
            user_name=row.get("user_name"),
            user_avatar=row.get("user_avatar"),
            user_role=row.get("user_role")
        )

    @classmethod
    def get_by_floorplan(cls, floorplan_id: int) -> List["Comment"]:
        """Retrieve comment threads for a floorplan."""
        query = """
            SELECT c.*, u.full_name as user_name, u.avatar_url as user_avatar, u.role as user_role 
            FROM comments c 
            JOIN users u ON c.user_id = u.id 
            WHERE c.floorplan_id = ? 
            ORDER BY c.created_at ASC;
        """
        rows = get_db().query_all(query, (floorplan_id,))
        return [cls.from_row(r) for r in rows]

    @classmethod
    def create(cls, **kwargs) -> "Comment":
        """Create new comment or reply."""
        db = get_db()
        c_id = db.execute(
            """INSERT INTO comments 
               (project_id, floorplan_id, user_id, pos_x, pos_y, comment_text, status, parent_id) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?);""",
            (
                kwargs["project_id"], kwargs.get("floorplan_id"), kwargs["user_id"],
                kwargs.get("pos_x"), kwargs.get("pos_y"), kwargs["comment_text"].strip(),
                kwargs.get("status", "Open"), kwargs.get("parent_id")
            )
        )
        row = db.query_one(
            """SELECT c.*, u.full_name as user_name, u.avatar_url as user_avatar, u.role as user_role 
               FROM comments c JOIN users u ON c.user_id = u.id WHERE c.id = ?;""",
            (c_id,)
        )
        return cls.from_row(row)
