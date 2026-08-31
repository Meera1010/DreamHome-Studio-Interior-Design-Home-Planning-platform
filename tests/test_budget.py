"""
DreamHome Studio — Budget & Cost Engine Unit Tests
Tests budget calculations, tax rates, designer margins, labor additions, and CSV export.
"""

import unittest
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from config import config
from database.db_manager import DatabaseManager, get_db
from backend.models.user import User
from backend.models.project import Project
from backend.models.budget import Budget, BudgetLineItem
from backend.services.cost_calculator_service import CostCalculatorService
from backend.services.report_generator import ReportGeneratorService

class TestBudgetEngine(unittest.TestCase):
    """Test suite for interior cost calculations and budget management."""

    @classmethod
    def setUpClass(cls):
        cls.db_path = config["testing"].DATABASE_PATH
        cls.db = get_db(cls.db_path)
        cls.db.init_db()

    def setUp(self):
        self.db.execute("DELETE FROM budget_line_items;")
        self.db.execute("DELETE FROM budgets;")
        self.db.execute("DELETE FROM projects;")
        self.db.execute("DELETE FROM users;")

        self.user = User.create("designer@test.com", "Pass123!", "Designer", "Designer")
        self.project = Project.create("Test Villa", self.user.id, budget_limit=50000.0)
        
        # Create budget record
        self.budget_id = self.db.execute(
            "INSERT INTO budgets (project_id, total_estimated, total_spent, tax_rate, labor_cost, designer_margin) VALUES (?, 0, 0, 0.085, 1000.0, 0.15);",
            (self.project.id,)
        )

    def test_budget_recalculation(self):
        """Test recalculating budget totals after adding line items."""
        # Add line items: Sofa $1850 x 1, Chairs $200 x 4 = $800 -> Subtotal = $2650
        self.db.execute(
            "INSERT INTO budget_line_items (budget_id, item_name, category, item_type, unit_price, quantity, total_price, status) VALUES (?, 'Sofa', 'Living', 'Furniture', 1850.0, 1, 1850.0, 'Purchased');",
            (self.budget_id,)
        )
        self.db.execute(
            "INSERT INTO budget_line_items (budget_id, item_name, category, item_type, unit_price, quantity, total_price, status) VALUES (?, 'Chairs', 'Dining', 'Furniture', 200.0, 4, 800.0, 'Estimated');",
            (self.budget_id,)
        )

        budget = Budget.from_row(self.db.query_one("SELECT * FROM budgets WHERE id = ?;", (self.budget_id,)))
        budget.recalculate_totals()

        # Items Subtotal: $2650 + Labor $1000 = $3650 before tax/margin
        # Tax (8.5%): $310.25
        # Margin (15%): $547.50
        # Grand Total Estimated: $3650 + $310.25 + $547.50 = $4507.75
        self.assertEqual(budget.total_estimated, 4507.75)
        
        # Spent should only include 'Purchased' sofa = $1850.00
        self.assertEqual(budget.total_spent, 1850.0)

    def test_cost_calculator_service(self):
        """Test dynamic floorplan cost calculator service."""
        canvas_data = {
            "room": {"width_m": 8.0, "height_m": 6.0},
            "walls": [{"x1": 50, "y1": 50, "x2": 450, "y2": 50}],
            "objects": [{"name": "Bed", "price": 2200.0}]
        }

        cost_data = CostCalculatorService.calculate_floorplan_costs(canvas_data)
        self.assertIn("summary", cost_data)
        self.assertGreater(cost_data["summary"]["grand_total"], 2200.0)

    def test_csv_report_generation(self):
        """Test exporting budget to CSV format."""
        csv_text = ReportGeneratorService.generate_budget_csv(self.budget_id)
        self.assertIn("Item Name", csv_text)
        self.assertIn("Unit Price", csv_text)

if __name__ == "__main__":
    unittest.main()
