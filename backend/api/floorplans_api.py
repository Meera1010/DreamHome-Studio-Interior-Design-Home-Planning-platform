"""
DreamHome Studio — Floorplans REST API
Endpoints for 2D room floorplans, saving canvas JSON, snapshotting versions, and SVG exports.
"""

from flask import Blueprint, request, jsonify, Response
from backend.models.floorplan import Floorplan
from backend.models.project import Project
from backend.models.audit_log import AuditLog
from backend.auth.security import login_required, get_current_user
from backend.services.geometry_service import GeometryService
from backend.services.cost_calculator_service import CostCalculatorService
from backend.services.floorplan_exporter import FloorplanExporterService
from backend.utils.validators import validate_required_fields

floorplans_bp = Blueprint("floorplans_api", __name__, url_prefix="/api/floorplans")

@floorplans_bp.route("/project/<int:project_id>", methods=["GET"])
@login_required
def list_project_floorplans(project_id: int):
    """Retrieve list of floorplans for a project."""
    project = Project.get_by_id(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
        
    floorplans = Floorplan.get_by_project(project_id)
    return jsonify({"floorplans": [fp.to_dict() for fp in floorplans]}), 200

@floorplans_bp.route("/<int:floorplan_id>", methods=["GET"])
@login_required
def get_floorplan(floorplan_id: int):
    """Retrieve single floorplan and detailed canvas layout payload."""
    fp = Floorplan.get_by_id(floorplan_id)
    if not fp:
        return jsonify({"error": "Floorplan not found"}), 404
        
    fp_dict = fp.to_dict()
    # Attach computed spatial math summary
    fp_dict["room_summary"] = GeometryService.calculate_room_summary_from_canvas(fp_dict["canvas_data"])
    fp_dict["cost_breakdown"] = CostCalculatorService.calculate_floorplan_costs(fp_dict["canvas_data"])
    return jsonify({"floorplan": fp_dict}), 200

@floorplans_bp.route("", methods=["POST"])
@login_required
def create_floorplan():
    """Create a new 2D room floorplan layout."""
    data = request.get_json() or {}
    valid, err = validate_required_fields(data, ["project_id", "name"])
    if not valid:
        return jsonify({"error": err}), 400
        
    user = get_current_user()
    fp = Floorplan.create(
        project_id=data["project_id"],
        name=data["name"],
        room_type=data.get("room_type", "Living Room"),
        width_m=float(data.get("width_m", 8.0)),
        height_m=float(data.get("height_m", 6.0)),
        canvas_data=data.get("canvas_data")
    )
    
    AuditLog.log("FLOORPLAN_CREATE", "Floorplan", fp.id, user.id, {"name": fp.name})
    return jsonify({"message": "Floorplan created successfully", "floorplan": fp.to_dict()}), 201

@floorplans_bp.route("/<int:floorplan_id>/save", methods=["POST"])
@login_required
def save_floorplan_canvas(floorplan_id: int):
    """Save updated canvas JSON payload and snapshot version history."""
    fp = Floorplan.get_by_id(floorplan_id)
    if not fp:
        return jsonify({"error": "Floorplan not found"}), 404
        
    user = get_current_user()
    data = request.get_json() or {}
    canvas_data = data.get("canvas_data")
    if not canvas_data:
        return jsonify({"error": "Missing canvas_data JSON payload"}), 400
        
    version_title = data.get("title", f"v{fp.version_number + 1}.0 Saved Draft")
    version_notes = data.get("notes", "User saved 2D canvas layout update")
    
    fp.save_version(version_title, version_notes, canvas_data, user.id)
    AuditLog.log("FLOORPLAN_SAVE", "Floorplan", fp.id, user.id, {"version": fp.version_number})
    
    updated_fp = Floorplan.get_by_id(floorplan_id)
    return jsonify({
        "message": "Floorplan layout saved successfully",
        "floorplan": updated_fp.to_dict()
    }), 200

@floorplans_bp.route("/<int:floorplan_id>/versions", methods=["GET"])
@login_required
def get_version_history(floorplan_id: int):
    """Retrieve full version history snapshots for a floorplan."""
    versions = Floorplan.get_version_history(floorplan_id)
    return jsonify({"versions": versions}), 200

@floorplans_bp.route("/<int:floorplan_id>/export/svg", methods=["GET"])
@login_required
def export_svg(floorplan_id: int):
    """Export floorplan canvas to standalone vector SVG XML file."""
    fp = Floorplan.get_by_id(floorplan_id)
    if not fp:
        return jsonify({"error": "Floorplan not found"}), 404
        
    fp_dict = fp.to_dict()
    svg_content = FloorplanExporterService.export_to_svg(fp_dict["canvas_data"])
    return Response(svg_content, mimetype="image/svg+xml")
