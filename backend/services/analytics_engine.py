"""
DreamHome Studio — Analytics Engine Service
Computes SaaS performance metrics, project status distributions, budget analytics,
catalog popularity statistics, and designer activity KPIs.
"""

from typing import Dict, Any, List
from database.db_manager import get_db

class AnalyticsEngineService:
    """SaaS analytics and aggregation engine."""

    @staticmethod
    def get_dashboard_analytics() -> Dict[str, Any]:
        """Aggregate high-level SaaS metrics for dashboard display."""
        db = get_db()
        
        total_projects = db.count("projects")
        active_projects = db.count("projects", "status IN ('In Design', 'In Progress', 'Pending Approval')")
        total_clients = db.count("users", "role = 'Client'")
        total_designers = db.count("users", "role = 'Designer'")
        total_floorplans = db.count("floorplans", "is_active = 1")

        # Project Status Distribution
        status_rows = db.query_all("SELECT status, COUNT(*) as count FROM projects GROUP BY status;")
        project_status_breakdown = {row["status"]: row["count"] for row in status_rows}

        # Total Financial Budget Summary
        budget_summary = db.query_one(
            "SELECT SUM(total_estimated) as total_est, SUM(total_spent) as total_spent FROM budgets;"
        )
        total_estimated = float(budget_summary["total_est"] or 0.0)
        total_spent = float(budget_summary["total_spent"] or 0.0)

        # Popular Furniture Categories
        cat_rows = db.query_all(
            "SELECT category, COUNT(*) as item_count FROM furniture_catalog GROUP BY category ORDER BY item_count DESC LIMIT 5;"
        )
        popular_categories = [{ "category": r["category"], "count": r["item_count"] } for r in cat_rows]

        # Recent Activity Feed
        recent_logs = db.query_all(
            """SELECT a.action, a.entity_type, a.created_at, u.full_name as user_name 
               FROM audit_logs a LEFT JOIN users u ON a.user_id = u.id 
               ORDER BY a.id DESC LIMIT 6;"""
        )

        return {
            "kpis": {
                "total_projects": total_projects,
                "active_projects": active_projects,
                "total_clients": total_clients,
                "total_designers": total_designers,
                "total_floorplans": total_floorplans,
                "total_estimated_budget": total_estimated,
                "total_spent_budget": total_spent
            },
            "project_status_breakdown": project_status_breakdown,
            "popular_categories": popular_categories,
            "recent_activities": recent_logs
        }
