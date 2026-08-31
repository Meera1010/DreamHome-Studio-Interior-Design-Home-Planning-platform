"""
DreamHome Studio — Moodboard REST API
Endpoints for design inspiration collages, color palette extractors, and visual swatches.
"""

from flask import Blueprint, request, jsonify
from backend.models.moodboard import Moodboard
from backend.auth.security import login_required, get_current_user
from backend.utils.validators import validate_required_fields

moodboard_bp = Blueprint("moodboard_api", __name__, url_prefix="/api/moodboards")

@moodboard_bp.route("/project/<int:project_id>", methods=["GET"])
@login_required
def list_project_moodboards(project_id: int):
    """Retrieve moodboards for a project."""
    boards = Moodboard.get_by_project(project_id)
    return jsonify({"moodboards": [b.to_dict() for b in boards]}), 200

@moodboard_bp.route("", methods=["POST"])
@login_required
def create_moodboard():
    """Create a new design moodboard."""
    data = request.get_json() or {}
    valid, err = validate_required_fields(data, ["project_id", "title"])
    if not valid:
        return jsonify({"error": err}), 400
        
    user = get_current_user()
    data["created_by"] = user.id
    board = Moodboard.create(**data)
    return jsonify({"message": "Moodboard created", "moodboard": board.to_dict()}), 201
