"""
DreamHome Studio — Collaboration, Comments & Approvals REST API
Endpoints for client-designer floorplan feedback pins, comments, and project approval requests.
"""

from flask import Blueprint, request, jsonify, session
from backend.models.comment import Comment
from backend.models.notification import Notification
from backend.models.audit_log import AuditLog
from backend.auth.security import login_required, get_current_user
from backend.utils.validators import validate_required_fields
from database.db_manager import get_db

collaboration_bp = Blueprint("collaboration_api", __name__, url_prefix="/api/collaboration")

@collaboration_bp.route("/floorplan/<int:floorplan_id>/comments", methods=["GET"])
@login_required
def get_floorplan_comments(floorplan_id: int):
    """Retrieve feedback comments and visual pin annotations for a floorplan."""
    comments = Comment.get_by_floorplan(floorplan_id)
    return jsonify({"comments": [c.to_dict() for c in comments]}), 200

@collaboration_bp.route("/comments", methods=["POST"])
@login_required
def add_comment():
    """Create a new feedback comment or visual coordinate pin on floorplan."""
    data = request.get_json() or {}
    valid, err = validate_required_fields(data, ["project_id", "comment_text"])
    if not valid:
        return jsonify({"error": err}), 400
        
    user = get_current_user()
    comment = Comment.create(
        project_id=data["project_id"],
        floorplan_id=data.get("floorplan_id"),
        user_id=user.id,
        pos_x=data.get("pos_x"),
        pos_y=data.get("pos_y"),
        comment_text=data["comment_text"],
        parent_id=data.get("parent_id")
    )

    AuditLog.log("COMMENT_ADDED", "Comment", comment.id, user.id)
    return jsonify({"message": "Comment posted successfully", "comment": comment.to_dict()}), 201

@collaboration_bp.route("/approvals", methods=["POST"])
@login_required
def submit_approval_request():
    """Submit a floorplan layout to client for formal design approval."""
    data = request.get_json() or {}
    valid, err = validate_required_fields(data, ["project_id", "floorplan_id"])
    if not valid:
        return jsonify({"error": err}), 400
        
    user = get_current_user()
    db = get_db()
    
    app_id = db.execute(
        """INSERT INTO approval_requests 
           (project_id, floorplan_id, requested_by, status, reviewer_notes) 
           VALUES (?, ?, ?, 'Pending', ?);""",
        (data["project_id"], data["floorplan_id"], user.id, data.get("notes", "Submitted for client review"))
    )
    
    AuditLog.log("APPROVAL_SUBMITTED", "ApprovalRequest", app_id, user.id)
    return jsonify({"message": "Approval request submitted", "approval_id": app_id}), 201
