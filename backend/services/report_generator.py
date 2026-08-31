"""
DreamHome Studio — Report Generator Service
Generates structured JSON, CSV text reports, and printable HTML summaries for budgets,
inventory stocks, project timelines, and client estimates.
"""

import io
import csv
from typing import Dict, Any, List
from backend.models.project import Project
from backend.models.budget import Budget
from backend.models.inventory import InventoryItem

class ReportGeneratorService:
    """Report generation engine for SaaS data export."""

    @staticmethod
    def generate_budget_csv(budget_id: int) -> str:
        """Generate CSV report string for budget line items."""
        from database.db_manager import get_db
        db = get_db()
        row = db.query_one("SELECT * FROM budgets WHERE id = ?;", (budget_id,))
        if not row:
            return "Item Name,Category,Type,Unit Price,Quantity,Total Price,Status\n"
            
        budget = Budget.from_row(row)

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Item Name", "Category", "Item Type", "Unit Price ($)", "Quantity", "Total Price ($)", "Status"])

        for item in budget.line_items:
            writer.writerow([
                item.item_name, item.category, item.item_type,
                f"{item.unit_price:.2f}", item.quantity,
                f"{item.total_price:.2f}", item.status
            ])

        writer.writerow([])
        writer.writerow(["Subtotal / Estimated", "", "", "", "", f"{budget.total_estimated:.2f}", ""])
        writer.writerow(["Total Spent", "", "", "", "", f"{budget.total_spent:.2f}", ""])
        return output.getvalue()

    @staticmethod
    def generate_inventory_csv() -> str:
        """Generate CSV report string for warehouse inventory."""
        items = InventoryItem.get_all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["SKU", "Furniture Name", "Supplier", "In Stock Qty", "Reorder Level", "Unit Cost ($)", "Location", "Status"])

        for item in items:
            writer.writerow([
                item.sku, item.furniture_name, item.supplier_name,
                item.quantity_in_stock, item.reorder_level,
                f"{item.unit_cost:.2f}", item.bin_location, item.status
            ])

        return output.getvalue()

    @staticmethod
    def generate_project_summary(project_id: int) -> Dict[str, Any]:
        """Generate comprehensive JSON summary payload for a project."""
        project = Project.get_by_id(project_id)
        if not project:
            return {"error": "Project not found"}

        budget = Budget.get_by_project_id(project_id)
        budget_dict = budget.to_dict() if budget else {}

        return {
            "project": project.to_dict(),
            "budget": budget_dict,
            "report_generated_at": str(project.updated_at)
        }
