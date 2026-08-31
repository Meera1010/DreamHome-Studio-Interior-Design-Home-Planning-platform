"""
DreamHome Studio — Reports & Export REST API
Endpoints for generating CSV reports for budgets, inventory, and project summaries.
"""

from flask import Blueprint, jsonify, Response
from backend.auth.security import login_required
from backend.services.report_generator import ReportGeneratorService

reports_bp = Blueprint("reports_api", __name__, url_prefix="/api/reports")

@reports_bp.route("/inventory/csv", methods=["GET"])
@login_required
def export_inventory_csv():
    """Export warehouse inventory listing to CSV."""
    csv_data = ReportGeneratorService.generate_inventory_csv()
    return Response(csv_data, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=inventory_report.csv"})

@reports_bp.route("/project/<int:project_id>/summary", methods=["GET"])
@login_required
def get_project_report_summary(project_id: int):
    """Retrieve full project summary JSON report."""
    summary = ReportGeneratorService.generate_project_summary(project_id)
    return jsonify({"report": summary}), 200
