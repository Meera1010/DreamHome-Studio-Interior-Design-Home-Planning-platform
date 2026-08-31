"""
DreamHome Studio — Tasks & Project Timeline REST API
Endpoints for managing project tasks, deadlines, priorities, and Gantt timeline items.
"""

from flask import Blueprint, request, jsonify
from backend.models.task import Task
from backend.auth.security import login_required, get_current_user
from backend.utils.validators import validate_required_fields
from database.db_manager import get_db

tasks_bp = Blueprint("tasks_api", __name__, url_prefix="/api/tasks")

@tasks_bp.route("/project/<int:project_id>", methods=["GET"])
@login_required
def get_project_tasks(project_id: int):
    """Retrieve tasks for a project."""
    tasks = Task.get_by_project(project_id)
    return jsonify({"tasks": [t.to_dict() for t in tasks]}), 200

@tasks_bp.route("", methods=["POST"])
@login_required
def create_task():
    """Create a new task."""
    data = request.get_json() or {}
    valid, err = validate_required_fields(data, ["project_id", "title"])
    if not valid:
        return jsonify({"error": err}), 400
        
    task = Task.create(**data)
    return jsonify({"message": "Task created", "task": task.to_dict()}), 201

@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@login_required
def update_task(task_id: int):
    """Update task status, hours, or assignment."""
    data = request.get_json() or {}
    task = Task.get_by_id(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
        
    allowed = {"title", "description", "assigned_to", "priority", "status", "due_date", "estimated_hours", "actual_hours"}
    updates = []
    params = []
    for k, v in data.items():
        if k in allowed:
            updates.append(f"{k} = ?")
            params.append(v)
            
    if updates:
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(task_id)
        get_db().execute(f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?;", tuple(params))
        
    updated_task = Task.get_by_id(task_id)
    return jsonify({"message": "Task updated", "task": updated_task.to_dict()}), 200
