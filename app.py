"""
DreamHome Studio — Main Application Entrypoint
Configures Flask WSGI app, database initialization, REST API blueprints registration,
error handling, and static template rendering routes.
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, jsonify, send_from_directory, request

# Add project root directory to python sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from config import config
from database.db_manager import get_db
from backend.api import (
    auth_bp, projects_bp, floorplans_bp, catalog_bp, inventory_bp,
    suppliers_bp, budget_bp, collaboration_bp, tasks_bp, moodboard_bp,
    portfolio_bp, reports_bp, analytics_bp, admin_bp, notifications_bp
)

def create_app(config_name="development"):
    """Application factory for DreamHome Studio Flask App."""
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates"
    )

    # Load Configuration
    cfg_class = config.get(config_name, config["default"])
    app.config.from_object(cfg_class)

    # Initialize Database Schema if needed
    db = get_db(app.config["DATABASE_PATH"])
    db.init_db()

    # Register REST API Blueprints
    blueprints = [
        auth_bp, projects_bp, floorplans_bp, catalog_bp, inventory_bp,
        suppliers_bp, budget_bp, collaboration_bp, tasks_bp, moodboard_bp,
        portfolio_bp, reports_bp, analytics_bp, admin_bp, notifications_bp
    ]
    for bp in blueprints:
        app.register_blueprint(bp)

    # HTML View Routes
    @app.route("/")
    def index():
        return render_template("base.html")

    @app.route("/health")
    def health_check():
        return jsonify({
            "status": "healthy",
            "app": "DreamHome Studio",
            "version": "1.0.0",
            "database": "connected"
        }), 200

    # Global Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Resource not found", "code": "NOT_FOUND"}), 404
        return render_template("base.html"), 200

    @app.errorhandler(500)
    def internal_error(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Internal server error", "code": "SERVER_ERROR"}), 500
        return render_template("base.html"), 500

    return app

app = create_app(os.environ.get("FLASK_ENV", "development"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting DreamHome Studio SaaS Server on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
