"""
DreamHome Studio — Full REST API End-to-End Integration Tests
Tests Flask API routes for Auth, Projects, Floorplans, Catalog, Inventory, Suppliers, Budget, Tasks, Analytics.
"""

import unittest
import os
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app import create_app
from config import config
from database.db_manager import DatabaseManager

class TestAPIEndpoints(unittest.TestCase):
    """End-to-end integration test suite for REST API blueprints."""

    @classmethod
    def setUpClass(cls):
        os.environ["FLASK_ENV"] = "testing"
        cls.app = create_app("testing")
        cls.client = cls.app.test_client()
        cls.db_path = config["testing"].DATABASE_PATH
        cls.db = DatabaseManager(cls.db_path)

    def setUp(self):
        """Seed seed_data for integration test requests."""
        from database.seed_data import seed_database
        seed_database(self.db_path)

    def test_health_check(self):
        """Test /health status endpoint."""
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["status"], "healthy")

    def test_auth_login_flow(self):
        """Test authentication login endpoint."""
        payload = {"email": "sarah.jenkins@dreamhome.com", "password": "Designer123!Password"}
        res = self.client.post("/api/auth/login", json=payload)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn("user", data)
        self.assertEqual(data["user"]["full_name"], "Sarah Jenkins")

    def test_catalog_furniture_endpoint(self):
        """Test furniture catalog search endpoint."""
        res = self.client.get("/api/catalog/furniture")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn("furniture", data)
        self.assertGreater(len(data["furniture"]), 0)

    def test_catalog_materials_endpoint(self):
        """Test material catalog endpoint."""
        res = self.client.get("/api/catalog/materials")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn("materials", data)
        self.assertGreater(len(data["materials"]), 0)

    def test_analytics_dashboard_endpoint(self):
        """Test dashboard metrics endpoint with logged in session."""
        with self.client.session_transaction() as sess:
            sess["user_id"] = 1
            sess["role"] = "Admin"

        res = self.client.get("/api/analytics/dashboard")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn("analytics", data)
        self.assertIn("kpis", data["analytics"])

if __name__ == "__main__":
    unittest.main()
