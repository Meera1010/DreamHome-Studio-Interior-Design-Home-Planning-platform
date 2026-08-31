"""
DreamHome Studio — Furniture & Material Catalog REST API
Endpoints for searching furniture items, filtering categories, and fetching materials.
"""

from flask import Blueprint, request, jsonify
from backend.models.furniture import FurnitureCatalog
from backend.models.material import MaterialCatalog
from backend.auth.security import login_required

catalog_bp = Blueprint("catalog_api", __name__, url_prefix="/api/catalog")

@catalog_bp.route("/furniture", methods=["GET"])
def search_furniture():
    """Search and filter furniture catalog items."""
    category = request.args.get("category")
    search_q = request.args.get("q")
    max_p = request.args.get("max_price", type=float)
    
    items = FurnitureCatalog.get_all(category=category, search_query=search_q, max_price=max_p)
    return jsonify({"furniture": [i.to_dict() for i in items]}), 200

@catalog_bp.route("/furniture/<int:item_id>", methods=["GET"])
def get_furniture_item(item_id: int):
    """Retrieve single furniture catalog item."""
    item = FurnitureCatalog.get_by_id(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"furniture": item.to_dict()}), 200

@catalog_bp.route("/materials", methods=["GET"])
def search_materials():
    """Retrieve material catalog items (flooring, paint, tiles, fabric)."""
    category = request.args.get("category")
    items = MaterialCatalog.get_all(category=category)
    return jsonify({"materials": [m.to_dict() for m in items]}), 200
