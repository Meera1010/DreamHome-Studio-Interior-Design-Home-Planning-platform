"""
DreamHome Studio — Portfolio REST API
Endpoints for public designer showcases, portfolio showcases, views, and likes.
"""

from flask import Blueprint, jsonify
from backend.models.portfolio import Portfolio

portfolio_bp = Blueprint("portfolio_api", __name__, url_prefix="/api/portfolio")

@portfolio_bp.route("/public", methods=["GET"])
def get_public_portfolio():
    """Retrieve public portfolio showcases."""
    showcases = Portfolio.get_public_showcases()
    return jsonify({"portfolios": [p.to_dict() for p in showcases]}), 200
