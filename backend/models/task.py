"""
DreamHome Studio — Project Task Model
Handles task management, priority, assignment, estimated/actual hours, and deadlines.
"""

from typing import Optional, List, Dict, Any
from database.db_manager import get_db

class Task:
    """Task entity model."""

    def __init__(
        self,
        id: Optional[int] = None,
        project_id: int = 0,
        title: str = "",
        description: Optional[str] = None,
        assigned_to: Optional[int] = None,
        priority: str = "Medium",
        status: str = "To Do",
        due_date: Optional[str] = None,
        estimated_hours: float = 0.0,
        actual_hours: float = 0.0,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        assignee_name: Optional[str] = None
    ):
        self.id = id
        self.project_id = project_id
        self.title = title
        self.description = description
        self.assigned_to = assigned_to
        self.priority = priority
        self.status = status
        self.due_date = due_date
        self.estimated_hours = float(estimated_hours)
        self.actual_hours = float(actual_hours)
        self.created_at = created_at
        self.updated_at = updated_at
        self.assignee_name = assignee_name

    def to_dict(self) -> Dict[str, Any]:
        """Serialize task model."""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "assigned_to": self.assigned_to,
            "priority": self.priority,
            "status": self.status,
            "due_date": str(self.due_date) if self.due_date else None,
            "estimated_hours": self.estimated_hours,
            "actual_hours": self.actual_hours,
            "created_at": str(self.created_at) if self.created_at else None,
            "updated_at": str(self.updated_at) if self.updated_at else None,
            "assignee_name": self.assignee_name
        }

    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> "Task":
        """Construct task model from row."""
        return cls(
            id=row["id"],
            project_id=row["project_id"],
            title=row["title"],
            description=row.get("description"),
            assigned_to=row.get("assigned_to"),
            priority=row.get("priority", "Medium"),
            status=row.get("status", "To Do"),
            due_date=row.get("due_date"),
            estimated_hours=row.get("estimated_hours", 0.0),
            actual_hours=row.get("actual_hours", 0.0),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
            assignee_name=row.get("assignee_name")
        )

    @classmethod
    def get_by_project(cls, project_id: int) -> List["Task"]:
        """Retrieve tasks for a project."""
        query = """
            SELECT t.*, u.full_name as assignee_name 
            FROM tasks t 
            LEFT JOIN users u ON t.assigned_to = u.id 
            WHERE t.project_id = ? 
            ORDER BY t.due_date ASC, t.id DESC;
        """
        rows = get_db().query_all(query, (project_id,))
        return [cls.from_row(r) for r in rows]

    @classmethod
    def create(cls, **kwargs) -> "Task":
        """Create new task record."""
        db = get_db()
        task_id = db.execute(
            """INSERT INTO tasks 
               (project_id, title, description, assigned_to, priority, status, due_date, estimated_hours) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?);""",
            (
                kwargs["project_id"], kwargs["title"].strip(), kwargs.get("description"),
                kwargs.get("assigned_to"), kwargs.get("priority", "Medium"),
                kwargs.get("status", "To Do"), kwargs.get("due_date"),
                kwargs.get("estimated_hours", 0.0)
            )
        )
        return cls.get_by_id(task_id)

    @classmethod
    def get_by_id(cls, task_id: int) -> Optional["Task"]:
        """Retrieve task by ID."""
        query = """
            SELECT t.*, u.full_name as assignee_name 
            FROM tasks t 
            LEFT JOIN users u ON t.assigned_to = u.id 
            WHERE t.id = ?;
        """
        row = get_db().query_one(query, (task_id,))
        return cls.from_row(row) if row else None
