"""
DreamHome Studio — Floorplan Data Model
Handles 2D interactive room layout records, canvas JSON serialization, room dimensions,
and version snapshot creation.
"""

import json
from typing import Optional, List, Dict, Any
from database.db_manager import get_db

class Floorplan:
    """Floorplan entity model."""

    def __init__(
        self,
        id: Optional[int] = None,
        project_id: int = 0,
        name: str = "New Floorplan",
        room_type: str = "Living Room",
        width_m: float = 8.0,
        height_m: float = 6.0,
        grid_size_cm: int = 20,
        scale_factor: float = 50.0,
        canvas_data_json: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        version_number: int = 1,
        is_active: bool = True,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
    ):
        self.id = id
        self.project_id = project_id
        self.name = name
        self.room_type = room_type
        self.width_m = float(width_m)
        self.height_m = float(height_m)
        self.grid_size_cm = int(grid_size_cm)
        self.scale_factor = float(scale_factor)
        self.canvas_data_json = canvas_data_json or json.dumps({
            "room": {"name": name, "width_m": width_m, "height_m": height_m},
            "walls": [],
            "openings": [],
            "objects": [],
            "lighting": []
        })
        self.thumbnail_url = thumbnail_url or "/static/images/floorplans/default_thumb.png"
        self.version_number = int(version_number)
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> Dict[str, Any]:
        """Serialize floorplan to dictionary, parsing canvas JSON payload."""
        parsed_canvas = {}
        try:
            parsed_canvas = json.loads(self.canvas_data_json) if self.canvas_data_json else {}
        except Exception:
            parsed_canvas = {}

        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "room_type": self.room_type,
            "width_m": self.width_m,
            "height_m": self.height_m,
            "area_sqm": round(self.width_m * self.height_m, 2),
            "grid_size_cm": self.grid_size_cm,
            "scale_factor": self.scale_factor,
            "canvas_data": parsed_canvas,
            "thumbnail_url": self.thumbnail_url,
            "version_number": self.version_number,
            "is_active": bool(self.is_active),
            "created_at": str(self.created_at) if self.created_at else None,
            "updated_at": str(self.updated_at) if self.updated_at else None
        }

    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> "Floorplan":
        """Construct Floorplan model from database row."""
        return cls(
            id=row["id"],
            project_id=row["project_id"],
            name=row["name"],
            room_type=row.get("room_type", "Living Room"),
            width_m=row.get("width_m", 8.0),
            height_m=row.get("height_m", 6.0),
            grid_size_cm=row.get("grid_size_cm", 20),
            scale_factor=row.get("scale_factor", 50.0),
            canvas_data_json=row.get("canvas_data_json"),
            thumbnail_url=row.get("thumbnail_url"),
            version_number=row.get("version_number", 1),
            is_active=bool(row.get("is_active", 1)),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at")
        )

    @classmethod
    def get_by_id(cls, floorplan_id: int) -> Optional["Floorplan"]:
        """Retrieve floorplan by ID."""
        row = get_db().query_one("SELECT * FROM floorplans WHERE id = ?;", (floorplan_id,))
        return cls.from_row(row) if row else None

    @classmethod
    def get_by_project(cls, project_id: int) -> List["Floorplan"]:
        """Retrieve all active floorplans belonging to a project."""
        rows = get_db().query_all(
            "SELECT * FROM floorplans WHERE project_id = ? AND is_active = 1 ORDER BY updated_at DESC;",
            (project_id,)
        )
        return [cls.from_row(r) for r in rows]

    @classmethod
    def create(
        cls,
        project_id: int,
        name: str,
        room_type: str = "Living Room",
        width_m: float = 8.0,
        height_m: float = 6.0,
        canvas_data: Optional[Dict[str, Any]] = None
    ) -> "Floorplan":
        """Create new floorplan and initial version snapshot."""
        canvas_json = json.dumps(canvas_data) if canvas_data else json.dumps({
            "room": {"name": name, "width_m": width_m, "height_m": height_m},
            "walls": [], "openings": [], "objects": [], "lighting": []
        })
        db = get_db()
        fp_id = db.execute(
            """INSERT INTO floorplans 
               (project_id, name, room_type, width_m, height_m, canvas_data_json, version_number) 
               VALUES (?, ?, ?, ?, ?, ?, 1);""",
            (project_id, name.strip(), room_type, width_m, height_m, canvas_json)
        )
        # Create Version 1 snapshot
        db.execute(
            """INSERT INTO floorplan_versions (floorplan_id, version_number, title, notes, canvas_data_json) 
               VALUES (?, 1, 'v1.0 Initial Creation', 'Initial floorplan template', ?);""",
            (fp_id, canvas_json)
        )
        return cls.get_by_id(fp_id)

    def save_version(self, title: str, notes: str, canvas_data: Dict[str, Any], user_id: Optional[int] = None) -> int:
        """Create a new version snapshot and update active floorplan state."""
        self.version_number += 1
        canvas_json = json.dumps(canvas_data) if isinstance(canvas_data, dict) else str(canvas_data)
        self.canvas_data_json = canvas_json
        
        db = get_db()
        # Save version history
        v_id = db.execute(
            """INSERT INTO floorplan_versions (floorplan_id, version_number, title, notes, canvas_data_json, created_by) 
               VALUES (?, ?, ?, ?, ?, ?);""",
            (self.id, self.version_number, title, notes, canvas_json, user_id)
        )
        # Update floorplan active JSON & version count
        db.execute(
            """UPDATE floorplans 
               SET version_number = ?, canvas_data_json = ?, updated_at = CURRENT_TIMESTAMP 
               WHERE id = ?;""",
            (self.version_number, canvas_json, self.id)
        )
        return v_id

    @classmethod
    def get_version_history(cls, floorplan_id: int) -> List[Dict[str, Any]]:
        """Retrieve all version snapshots for a floorplan."""
        query = """
            SELECT fv.*, u.full_name as creator_name 
            FROM floorplan_versions fv 
            LEFT JOIN users u ON fv.created_by = u.id 
            WHERE fv.floorplan_id = ? 
            ORDER BY fv.version_number DESC;
        """
        return get_db().query_all(query, (floorplan_id,))

    def delete(self) -> bool:
        """Soft delete floorplan."""
        return get_db().execute("UPDATE floorplans SET is_active = 0 WHERE id = ?;", (self.id,)) > 0
