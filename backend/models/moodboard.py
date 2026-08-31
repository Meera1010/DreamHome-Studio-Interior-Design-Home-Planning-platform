"""
DreamHome Studio — Moodboard Model
Handles design inspiration collages, color palette swatches, and layout items.
"""

import json
from typing import Optional, List, Dict, Any
from database.db_manager import get_db

class Moodboard:
    """Moodboard entity model."""

    def __init__(
        self,
        id: Optional[int] = None,
        project_id: int = 0,
        title: str = "",
        description: Optional[str] = None,
        layout_json: Optional[str] = None,
        color_palette_json: Optional[str] = None,
        tags: Optional[str] = None,
        created_by: int = 0,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        creator_name: Optional[str] = None
    ):
        self.id = id
        self.project_id = project_id
        self.title = title
        self.description = description
        self.layout_json = layout_json or '{"grid": []}'
        self.color_palette_json = color_palette_json or '[]'
        self.tags = tags
        self.created_by = created_by
        self.created_at = created_at
        self.updated_at = updated_at
        self.creator_name = creator_name

    def to_dict(self) -> Dict[str, Any]:
        """Serialize moodboard model."""
        layout = {}
        palette = []
        try:
            layout = json.loads(self.layout_json) if self.layout_json else {}
            palette = json.loads(self.color_palette_json) if self.color_palette_json else []
        except Exception:
            pass

        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "layout": layout,
            "color_palette": palette,
            "tags": self.tags,
            "created_by": self.created_by,
            "created_at": str(self.created_at) if self.created_at else None,
            "updated_at": str(self.updated_at) if self.updated_at else None,
            "creator_name": self.creator_name
        }

    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> "Moodboard":
        """Construct moodboard model from row."""
        return cls(
            id=row["id"],
            project_id=row["project_id"],
            title=row["title"],
            description=row.get("description"),
            layout_json=row.get("layout_json"),
            color_palette_json=row.get("color_palette_json"),
            tags=row.get("tags"),
            created_by=row["created_by"],
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
            creator_name=row.get("creator_name")
        )

    @classmethod
    def get_by_project(cls, project_id: int) -> List["Moodboard"]:
        """Retrieve moodboards for a project."""
        query = """
            SELECT m.*, u.full_name as creator_name 
            FROM moodboards m 
            JOIN users u ON m.created_by = u.id 
            WHERE m.project_id = ? 
            ORDER BY m.updated_at DESC;
        """
        rows = get_db().query_all(query, (project_id,))
        return [cls.from_row(r) for r in rows]

    @classmethod
    def create(cls, **kwargs) -> "Moodboard":
        """Create new moodboard."""
        layout_json = json.dumps(kwargs.get("layout", {}))
        palette_json = json.dumps(kwargs.get("color_palette", []))
        
        db = get_db()
        mb_id = db.execute(
            """INSERT INTO moodboards 
               (project_id, title, description, layout_json, color_palette_json, tags, created_by) 
               VALUES (?, ?, ?, ?, ?, ?, ?);""",
            (
                kwargs["project_id"], kwargs["title"].strip(), kwargs.get("description"),
                layout_json, palette_json, kwargs.get("tags"), kwargs["created_by"]
            )
        )
        row = db.query_one("SELECT m.*, u.full_name as creator_name FROM moodboards m JOIN users u ON m.created_by = u.id WHERE m.id = ?;", (mb_id,))
        return cls.from_row(row)
