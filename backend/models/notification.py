"""
DreamHome Studio — Notification Model
Handles user notifications, unread counts, and activity alerts.
"""

from typing import Optional, List, Dict, Any
from database.db_manager import get_db

class Notification:
    """Notification entity model."""

    def __init__(
        self,
        id: Optional[int] = None,
        user_id: int = 0,
        title: str = "",
        message: str = "",
        type: str = "Info",
        is_read: bool = False,
        target_url: Optional[str] = None,
        created_at: Optional[str] = None
    ):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.message = message
        self.type = type
        self.is_read = is_read
        self.target_url = target_url
        self.created_at = created_at

    def to_dict(self) -> Dict[str, Any]:
        """Serialize notification model."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "message": self.message,
            "type": self.type,
            "is_read": bool(self.is_read),
            "target_url": self.target_url,
            "created_at": str(self.created_at) if self.created_at else None
        }

    @classmethod
    def get_by_user(cls, user_id: int, limit: int = 20) -> List["Notification"]:
        """Retrieve notifications for a user."""
        query = "SELECT * FROM notifications WHERE user_id = ? ORDER BY id DESC LIMIT ?;"
        rows = get_db().query_all(query, (user_id, limit))
        return [
            cls(
                id=r["id"], user_id=r["user_id"], title=r["title"],
                message=r["message"], type=r.get("type", "Info"),
                is_read=bool(r.get("is_read", 0)), target_url=r.get("target_url"),
                created_at=r.get("created_at")
            ) for r in rows
        ]

    @classmethod
    def create(cls, user_id: int, title: str, message: str, type: str = "Info", target_url: Optional[str] = None) -> "Notification":
        """Create new notification record."""
        db = get_db()
        n_id = db.execute(
            "INSERT INTO notifications (user_id, title, message, type, target_url) VALUES (?, ?, ?, ?, ?);",
            (user_id, title.strip(), message.strip(), type, target_url)
        )
        row = db.query_one("SELECT * FROM notifications WHERE id = ?;", (n_id,))
        return cls(
            id=row["id"], user_id=row["user_id"], title=row["title"],
            message=row["message"], type=row.get("type", "Info"),
            is_read=bool(row.get("is_read", 0)), target_url=row.get("target_url"),
            created_at=row.get("created_at")
        )

    @classmethod
    def mark_all_as_read(cls, user_id: int) -> int:
        """Mark all notifications as read for a user."""
        return get_db().execute("UPDATE notifications SET is_read = 1 WHERE user_id = ?;", (user_id,))
