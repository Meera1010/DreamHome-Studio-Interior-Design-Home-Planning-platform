"""
DreamHome Studio — Projects Unit Tests
Tests project creation, client/designer linkage, status filtering, and budget linkage.
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

class TestProjects(unittest.TestCase):
    """Test suite for Project domain model."""

    @classmethod
    def setUpClass(cls):
        cls.db_path = config["testing"].DATABASE_PATH
        cls.db = get_db(cls.db_path)
        cls.db.init_db()

    def setUp(self):
        self.db.execute("DELETE FROM projects;")
        self.db.execute("DELETE FROM users;")
        
        self.designer = User.create("designer@test.com", "Pass123!", "Lead Designer", "Designer")
        self.client = User.create("client@test.com", "Pass123!", "Client User", "Client")

    def test_create_project(self):
        """Test creating a project with client and designer links."""
        project = Project.create(
            title="Luxury Villa Renovation",
            designer_id=self.designer.id,
            client_id=self.client.id,
            description="Full home space planning",
            budget_limit=150000.0,
            status="In Design"
        )

        self.assertIsNotNone(project.id)
        self.assertEqual(project.title, "Luxury Villa Renovation")
        self.assertEqual(project.designer_id, self.designer.id)
        self.assertEqual(project.client_id, self.client.id)
        self.assertEqual(project.budget_limit, 150000.0)
        self.assertEqual(project.status, "In Design")

    def test_project_retrieval_and_filtering(self):
        """Test retrieving projects filtered by designer vs client."""
        p1 = Project.create("Project 1", self.designer.id, client_id=self.client.id, status="Planning")
        p2 = Project.create("Project 2", self.designer.id, client_id=self.client.id, status="Approved")

        designer_projects = Project.get_all(user_id=self.designer.id, role="Designer")
        self.assertEqual(len(designer_projects), 2)

        approved_projects = Project.get_all(status="Approved")
        self.assertEqual(len(approved_projects), 1)
        self.assertEqual(approved_projects[0].title, "Project 2")

    def test_update_project_status(self):
        """Test updating project status."""
        project = Project.create("Test Project", self.designer.id)
        updated = project.update(status="Completed", budget_limit=180000.0)
        
        self.assertEqual(updated.status, "Completed")
        self.assertEqual(updated.budget_limit, 180000.0)

if __name__ == "__main__":
    unittest.main()
