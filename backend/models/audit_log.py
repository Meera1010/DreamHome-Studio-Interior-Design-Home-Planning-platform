"""
DreamHome Studio — Security Audit Log Model
Records user events, system actions, IP addresses, user agents, and security mutations.
"""

import json
from typing import Optional, List, Dict, Any
from database.db_manager import get_db

class AuditLog:
    """Audit log entity model."""

    def __init__(
        self,
        id: Optional[int] = None,
        user_id: Optional[int] = None,
        action: str = "",
        entity_type: str = "",
        entity_id: Optional[int] = None,
        details_json: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        created_at: Optional[str] = None,
        user_name: Optional[str] = None
    ):
        self.id = id
        self.user_id = user_id
        self.action = action
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.details_json = details_json
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.created_at = created_at
        self.user_name = user_name

    def to_dict(self) -> Dict[str, Any]:
        """Serialize audit log model."""
        details = {}
        try:
            details = json.loads(self.details_json) if self.details_json else {}
        except Exception:
            pass

        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user_name or "System",
            "action": self.action,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "details": details,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": str(self.created_at) if self.created_at else None
        }

    @classmethod
    def log(
        cls,
        action: str,
        entity_type: str,
        entity_id: Optional[int] = None,
        user_id: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> "AuditLog":
        """Persist audit record to database."""
        details_json = json.dumps(details) if isinstance(details, dict) else str(details or "")
        db = get_db()
        log_id = db.execute(
            """INSERT INTO audit_logs 
               (user_id, action, entity_type, entity_id, details_json, ip_address, user_agent) 
               VALUES (?, ?, ?, ?, ?, ?, ?);""",
            (user_id, action, entity_type, entity_id, details_json, ip_address, user_agent)
        )
        row = db.query_one(
            """SELECT a.*, u.full_name as user_name 
               FROM audit_logs a LEFT JOIN users u ON a.user_id = u.id WHERE a.id = ?;""",
            (log_id,)
        )
        return cls(
            id=row["id"], user_id=row.get("user_id"), action=row["action"],
            entity_type=row["entity_type"], entity_id=row.get("entity_id"),
            details_json=row.get("details_json"), ip_address=row.get("ip_address"),
            user_agent=row.get("user_agent"), created_at=row.get("created_at"),
            user_name=row.get("user_name")
        )

    @classmethod
    def get_recent(cls, limit: int = 50) -> List["AuditLog"]:
        """Retrieve recent audit logs for Admin inspection."""
        query = """
            SELECT a.*, u.full_name as user_name 
            FROM audit_logs a 
            LEFT JOIN users u ON a.user_id = u.id 
            ORDER BY a.id DESC LIMIT ?;
        """
        rows = get_db().query_all(query, (limit,))
        return [
            cls(
                id=r["id"], user_id=r.get("user_id"), action=r["action"],
                entity_type=r["entity_type"], entity_id=r.get("entity_id"),
                details_json=r.get("details_json"), ip_address=r.get("ip_address"),
                user_agent=r.get("user_agent"), created_at=r.get("created_at"),
                user_name=r.get("user_name")
            ) for r in rows
        ]
