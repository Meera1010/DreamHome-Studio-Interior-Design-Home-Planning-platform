"""
DreamHome Studio — Collaboration & Commenting Unit Tests
Tests feedback comments, floorplan coordinate pins, and client approval requests.
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
from backend.models.floorplan import Floorplan
from backend.models.comment import Comment

class TestCollaboration(unittest.TestCase):
    """Test suite for client-designer collaboration features."""

    @classmethod
    def setUpClass(cls):
        cls.db_path = config["testing"].DATABASE_PATH
        cls.db = get_db(cls.db_path)
        cls.db.init_db()

    def setUp(self):
        self.db.execute("DELETE FROM comments;")
        self.db.execute("DELETE FROM floorplans;")
        self.db.execute("DELETE FROM projects;")
        self.db.execute("DELETE FROM users;")
        self.db.execute("DELETE FROM sqlite_sequence WHERE name IN ('comments', 'floorplans', 'projects', 'users');")

        self.designer = User.create("designer_collab@test.com", "Pass123!", "Designer", "Designer")
        self.client = User.create("client_collab@test.com", "Pass123!", "Client", "Client")
        self.project = Project.create("Penthouse Project", self.designer.id, client_id=self.client.id)
        self.floorplan = Floorplan.create(self.project.id, "Living Room Layout")

    def test_post_comment_and_coordinate_pin(self):
        """Test posting a feedback comment pinned to 2D canvas coordinates."""
        comment = Comment.create(
            project_id=self.project.id,
            floorplan_id=self.floorplan.id,
            user_id=self.client.id,
            pos_x=320.0,
            pos_y=240.0,
            comment_text="Can we switch the sofa color to navy velvet?"
        )

        self.assertIsNotNone(comment.id)
        self.assertEqual(comment.pos_x, 320.0)
        self.assertEqual(comment.pos_y, 240.0)
        self.assertEqual(comment.comment_text, "Can we switch the sofa color to navy velvet?")

        # Fetch comments for floorplan
        comments = Comment.get_by_floorplan(self.floorplan.id)
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].user_name, "Client")

if __name__ == "__main__":
    unittest.main()
