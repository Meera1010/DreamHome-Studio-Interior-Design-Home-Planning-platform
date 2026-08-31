"""
DreamHome Studio — Suppliers REST API
Endpoints for managing furniture suppliers, manufacturer ratings, and lead times.
"""

from flask import Blueprint, request, jsonify
from backend.models.supplier import Supplier
from backend.auth.security import login_required, role_required

suppliers_bp = Blueprint("suppliers_api", __name__, url_prefix="/api/suppliers")

@suppliers_bp.route("", methods=["GET"])
@login_required
def list_suppliers():
    """Retrieve list of suppliers."""
    suppliers = Supplier.get_all()
    return jsonify({"suppliers": [s.to_dict() for s in suppliers]}), 200

@suppliers_bp.route("/<int:supplier_id>", methods=["GET"])
@login_required
def get_supplier(supplier_id: int):
    """Retrieve single supplier record."""
    supplier = Supplier.get_by_id(supplier_id)
    if not supplier:
        return jsonify({"error": "Supplier not found"}), 404
    return jsonify({"supplier": supplier.to_dict()}), 200

@suppliers_bp.route("", methods=["POST"])
@role_required("Designer", "Admin")
def create_supplier():
    """Create a new supplier profile."""
    data = request.get_json() or {}
    if "company_name" not in data:
        return jsonify({"error": "company_name is required"}), 400
    s = Supplier.create(**data)
    return jsonify({"message": "Supplier created", "supplier": s.to_dict()}), 201
