"""
DreamHome Studio — Floorplans Unit Tests
Tests 2D room floorplan creation, version snapshot history, canvas JSON serialization,
and SVG vector generation.
"""

import unittest
import os
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from config import config
from database.db_manager import DatabaseManager, get_db
from backend.models.user import User
from backend.models.project import Project
from backend.models.floorplan import Floorplan
from backend.services.floorplan_exporter import FloorplanExporterService

class TestFloorplans(unittest.TestCase):
    """Test suite for Floorplan model and version history."""

    @classmethod
    def setUpClass(cls):
        cls.db_path = config["testing"].DATABASE_PATH
        cls.db = get_db(cls.db_path)
        cls.db.init_db()

    def setUp(self):
        self.db.execute("DELETE FROM floorplan_versions;")
        self.db.execute("DELETE FROM floorplans;")
        self.db.execute("DELETE FROM projects;")
        self.db.execute("DELETE FROM users;")

        self.user = User.create("designer@test.com", "Pass123!", "Designer", "Designer")
        self.project = Project.create("Test Project", self.user.id)

    def test_create_floorplan_and_version(self):
        """Test floorplan creation initializes version 1 snapshot."""
        canvas_data = {
            "room": {"name": "Master Living Room", "width_m": 8.0, "height_m": 6.0},
            "walls": [{"x1": 50, "y1": 50, "x2": 450, "y2": 50}],
            "objects": [{"name": "Modern Sofa", "x": 100, "y": 100, "width": 200, "depth": 90}]
        }

        fp = Floorplan.create(
            project_id=self.project.id,
            name="Living Room Layout",
            room_type="Living Room",
            width_m=8.0,
            height_m=6.0,
            canvas_data=canvas_data
        )

        self.assertIsNotNone(fp.id)
        self.assertEqual(fp.name, "Living Room Layout")
        self.assertEqual(fp.version_number, 1)
        
        # Check auto-created version 1 history
        versions = Floorplan.get_version_history(fp.id)
        self.assertEqual(len(versions), 1)
        self.assertEqual(versions[0]["version_number"], 1)

    def test_save_new_version(self):
        """Test snapshotting new floorplan version increment."""
        fp = Floorplan.create(self.project.id, "Initial Draft", width_m=6.0, height_m=5.0)
        
        new_canvas = {
            "room": {"name": "Updated Room", "width_m": 6.0, "height_m": 5.0},
            "walls": [], "objects": [{"name": "Table", "x": 120, "y": 120}]
        }

        v_id = fp.save_version("v2.0 Revision", "Added dining table", new_canvas, self.user.id)
        self.assertIsNotNone(v_id)

        updated_fp = Floorplan.get_by_id(fp.id)
        self.assertEqual(updated_fp.version_number, 2)

        history = Floorplan.get_version_history(fp.id)
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["version_number"], 2)

    def test_svg_export(self):
        """Test exporting floorplan JSON to SVG string."""
        canvas_data = {
            "room": {"name": "Sample Room", "width_m": 6.0, "height_m": 5.0},
            "walls": [{"x1": 50, "y1": 50, "x2": 350, "y2": 50, "color": "#1e293b"}],
            "objects": [{"name": "Chair", "x": 100, "y": 100, "width": 50, "depth": 50, "color": "#6366f1"}]
        }

        svg = FloorplanExporterService.export_to_svg(canvas_data)
        self.assertIn('<svg', svg)
        self.assertIn('Sample Room', svg)
        self.assertIn('Chair', svg)
        self.assertIn('</svg>', svg)

if __name__ == "__main__":
    unittest.main()
