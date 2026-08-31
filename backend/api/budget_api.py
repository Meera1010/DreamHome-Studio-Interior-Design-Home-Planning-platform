"""
DreamHome Studio — Budget & Cost Calculator REST API
Endpoints for managing project budgets, adding line items, recalculating totals, and exporting CSV.
"""

from flask import Blueprint, request, jsonify, Response
from backend.models.budget import Budget, BudgetLineItem
from backend.models.project import Project
from backend.auth.security import login_required
from backend.services.report_generator import ReportGeneratorService
from backend.utils.validators import validate_required_fields
from database.db_manager import get_db

budget_bp = Blueprint("budget_api", __name__, url_prefix="/api/budgets")

@budget_bp.route("/project/<int:project_id>", methods=["GET"])
@login_required
def get_project_budget(project_id: int):
    """Retrieve budget and line items for a project."""
    budget = Budget.get_by_project_id(project_id)
    if not budget:
        return jsonify({"error": "Budget not found"}), 404
    return jsonify({"budget": budget.to_dict()}), 200

@budget_bp.route("/<int:budget_id>/items", methods=["POST"])
@login_required
def add_budget_item(budget_id: int):
    """Add a new line item to budget and recalculate total."""
    data = request.get_json() or {}
    valid, err = validate_required_fields(data, ["item_name", "unit_price"])
    if not valid:
        return jsonify({"error": err}), 400
        
    db = get_db()
    qty = int(data.get("quantity", 1))
    u_price = float(data["unit_price"])
    total_price = round(u_price * qty, 2)
    
    db.execute(
        """INSERT INTO budget_line_items 
           (budget_id, item_name, category, item_type, unit_price, quantity, total_price, status) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?);""",
        (
            budget_id, data["item_name"].strip(), data.get("category", "Custom"),
            data.get("item_type", "Furniture"), u_price, qty, total_price,
            data.get("status", "Estimated")
        )
    )
    
    budget = Budget.from_row(db.query_one("SELECT * FROM budgets WHERE id = ?;", (budget_id,)))
    budget.recalculate_totals()
    return jsonify({"message": "Budget line item added", "budget": budget.to_dict()}), 201

@budget_bp.route("/<int:budget_id>/export/csv", methods=["GET"])
@login_required
def export_budget_csv(budget_id: int):
    """Export budget estimate to CSV string."""
    csv_data = ReportGeneratorService.generate_budget_csv(budget_id)
    return Response(csv_data, mimetype="text/csv", headers={"Content-Disposition": f"attachment;filename=budget_{budget_id}.csv"})
