"""
DreamHome Studio — Inventory REST API
Endpoints for tracking warehouse furniture stock levels, reorder thresholds, and location bins.
"""

from flask import Blueprint, request, jsonify
from backend.models.inventory import InventoryItem
from backend.auth.security import login_required, role_required

inventory_bp = Blueprint("inventory_api", __name__, url_prefix="/api/inventory")

@inventory_bp.route("", methods=["GET"])
@login_required
def list_inventory():
    """Retrieve warehouse inventory stock listing."""
    status_filter = request.args.get("status")
    items = InventoryItem.get_all(status_filter=status_filter)
    return jsonify({"inventory": [i.to_dict() for i in items]}), 200

@inventory_bp.route("/<int:item_id>", methods=["GET"])
@login_required
def get_inventory_item(item_id: int):
    """Retrieve single inventory stock record."""
    item = InventoryItem.get_by_id(item_id)
    if not item:
        return jsonify({"error": "Inventory record not found"}), 404
    return jsonify({"inventory_item": item.to_dict()}), 200
