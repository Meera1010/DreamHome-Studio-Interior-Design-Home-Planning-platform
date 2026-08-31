"""
DreamHome Studio — Admin Panel REST API
Endpoints for user management, role modification, deactivation, system audit logs, and DB backup stats.
"""

from flask import Blueprint, request, jsonify
from backend.models.user import User
from backend.models.audit_log import AuditLog
from backend.auth.security import role_required, get_current_user

admin_bp = Blueprint("admin_api", __name__, url_prefix="/api/admin")

@admin_bp.route("/users", methods=["GET"])
@role_required("Admin")
def list_all_users():
    """Retrieve all users in system."""
    users = User.get_all(active_only=False)
    return jsonify({"users": [u.to_dict(include_private=False) for u in users]}), 200

@admin_bp.route("/users/<int:user_id>/role", methods=["PUT"])
@role_required("Admin")
def update_user_role(user_id: int):
    """Update role of a user."""
    data = request.get_json() or {}
    new_role = data.get("role")
    if new_role not in ("Designer", "Client", "Admin"):
        return jsonify({"error": "Invalid role specified"}), 400
        
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    updated = user.update(role=new_role)
    admin_user = get_current_user()
    AuditLog.log("ADMIN_ROLE_CHANGE", "User", user_id, admin_user.id, {"new_role": new_role})
    return jsonify({"message": "User role updated", "user": updated.to_dict()}), 200

@admin_bp.route("/users/<int:user_id>/status", methods=["PUT"])
@role_required("Admin")
def toggle_user_status(user_id: int):
    """Activate or deactivate user account."""
    data = request.get_json() or {}
    is_active = bool(data.get("is_active", True))
    
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    updated = user.update(is_active=is_active)
    admin_user = get_current_user()
    AuditLog.log("ADMIN_USER_STATUS", "User", user_id, admin_user.id, {"is_active": is_active})
    return jsonify({"message": f"User status set to {'Active' if is_active else 'Deactivated'}", "user": updated.to_dict()}), 200

@admin_bp.route("/audit-logs", methods=["GET"])
@role_required("Admin")
def get_audit_logs():
    """Retrieve system security audit logs."""
    limit = request.args.get("limit", default=50, type=int)
    logs = AuditLog.get_recent(limit=limit)
    return jsonify({"audit_logs": [l.to_dict() for l in logs]}), 200
