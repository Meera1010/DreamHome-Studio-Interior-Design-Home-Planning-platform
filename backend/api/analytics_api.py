"""
DreamHome Studio — Analytics REST API
Endpoints for SaaS KPI metrics, project status breakdowns, financial overview, and SVG charts.
"""

from flask import Blueprint, jsonify
from backend.services.analytics_engine import AnalyticsEngineService
from backend.auth.security import login_required

analytics_bp = Blueprint("analytics_api", __name__, url_prefix="/api/analytics")

@analytics_bp.route("/dashboard", methods=["GET"])
@login_required
def get_dashboard_metrics():
    """Retrieve high-level SaaS dashboard analytics."""
    data = AnalyticsEngineService.get_dashboard_analytics()
    return jsonify({"analytics": data}), 200
