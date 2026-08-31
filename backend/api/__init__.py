"""
DreamHome Studio — REST API Blueprints Package
"""

from backend.api.auth_api import auth_bp
from backend.api.projects_api import projects_bp
from backend.api.floorplans_api import floorplans_bp
from backend.api.catalog_api import catalog_bp
from backend.api.inventory_api import inventory_bp
from backend.api.suppliers_api import suppliers_bp
from backend.api.budget_api import budget_bp
from backend.api.collaboration_api import collaboration_bp
from backend.api.tasks_api import tasks_bp
from backend.api.moodboard_api import moodboard_bp
from backend.api.portfolio_api import portfolio_bp
from backend.api.reports_api import reports_bp
from backend.api.analytics_api import analytics_bp
from backend.api.admin_api import admin_bp
from backend.api.notifications_api import notifications_bp

__all__ = [
    "auth_bp",
    "projects_bp",
    "floorplans_bp",
    "catalog_bp",
    "inventory_bp",
    "suppliers_bp",
    "budget_bp",
    "collaboration_bp",
    "tasks_bp",
    "moodboard_bp",
    "portfolio_bp",
    "reports_bp",
    "analytics_bp",
    "admin_bp",
    "notifications_bp"
]
