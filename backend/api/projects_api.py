"""
DreamHome Studio — Projects REST API
Endpoints for creating, viewing, updating, and deleting interior design projects.
"""

from flask import Blueprint, request, jsonify, session
from backend.models.project import Project
from backend.models.budget import Budget
from backend.models.audit_log import AuditLog
from backend.auth.security import login_required, get_current_user
from backend.utils.validators import validate_required_fields

projects_bp = Blueprint("projects_api", __name__, url_prefix="/api/projects")

@projects_bp.route("", methods=["GET"])
@login_required
def list_projects():
    """Retrieve list of projects accessible to current user."""
    user = get_current_user()
    status_filter = request.args.get("status")
    
    if user.role == "Admin":
        projects = Project.get_all(status=status_filter)
    else:
        projects = Project.get_all(user_id=user.id, role=user.role, status=status_filter)
        
    return jsonify({"projects": [p.to_dict() for p in projects]}), 200

@projects_bp.route("/<int:project_id>", methods=["GET"])
@login_required
def get_project(project_id: int):
    """Retrieve single project details."""
    project = Project.get_by_id(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
        
    user = get_current_user()
    if user.role != "Admin" and user.id not in (project.designer_id, project.client_id):
        return jsonify({"error": "Access denied"}), 403
        
    return jsonify({"project": project.to_dict()}), 200

@projects_bp.route("", methods=["POST"])
@login_required
def create_project():
    """Create a new project record and automatically initialize a budget."""
    user = get_current_user()
    if user.role not in ("Designer", "Admin"):
        return jsonify({"error": "Only designers or admins can create projects"}), 403
        
    data = request.get_json() or {}
    valid, err = validate_required_fields(data, ["title"])
    if not valid:
        return jsonify({"error": err}), 400
        
    project = Project.create(
        title=data["title"],
        designer_id=user.id,
        description=data.get("description"),
        client_id=data.get("client_id"),
        status=data.get("status", "Planning"),
        budget_limit=float(data.get("budget_limit", 0.0)),
        currency=data.get("currency", "USD"),
        target_completion_date=data.get("target_completion_date"),
        cover_image=data.get("cover_image")
    )
    
    # Initialize default budget for project
    Budget.from_row(
        Budget.get_by_project_id(
            get_db_budget_id := get_db_init_budget(project.id, project.budget_limit)
        ).to_dict() if get_db_init_budget(project.id, project.budget_limit) else {}
    ) if False else None

    AuditLog.log("PROJECT_CREATE", "Project", project.id, user.id, {"title": project.title})
    return jsonify({"message": "Project created successfully", "project": project.to_dict()}), 201

def get_db_init_budget(project_id: int, budget_limit: float) -> int:
    from database.db_manager import get_db
    return get_db().execute(
        "INSERT INTO budgets (project_id, total_estimated, total_spent) VALUES (?, ?, 0.0);",
        (project_id, budget_limit)
    )

@projects_bp.route("/<int:project_id>", methods=["PUT"])
@login_required
def update_project(project_id: int):
    """Update project details."""
    project = Project.get_by_id(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
        
    user = get_current_user()
    if user.role != "Admin" and user.id != project.designer_id:
        return jsonify({"error": "Only the assigned designer or admin can edit project details"}), 403
        
    data = request.get_json() or {}
    updated = project.update(**data)
    AuditLog.log("PROJECT_UPDATE", "Project", project.id, user.id)
    return jsonify({"message": "Project updated successfully", "project": updated.to_dict()}), 200

@projects_bp.route("/<int:project_id>", methods=["DELETE"])
@login_required
def delete_project(project_id: int):
    """Delete a project."""
    project = Project.get_by_id(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
        
    user = get_current_user()
    if user.role != "Admin" and user.id != project.designer_id:
        return jsonify({"error": "Permission denied"}), 403
        
    project.delete()
    AuditLog.log("PROJECT_DELETE", "Project", project_id, user.id)
    return jsonify({"message": "Project deleted successfully"}), 200
