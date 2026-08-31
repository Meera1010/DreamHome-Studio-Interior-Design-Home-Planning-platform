"""
DreamHome Studio — Auth & Security Unit Tests
Tests user creation, password hashing, authentication credentials check,
role assignments, session state validation, and account deactivation rules.
"""

import unittest
import os
import sys
from pathlib import Path

# Add root directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from config import config
from database.db_manager import get_db, DatabaseManager
from backend.models.user import User

class TestAuthSecurity(unittest.TestCase):
    """Test suite for authentication and user security models."""

    @classmethod
    def setUpClass(cls):
        """Configure test database environment."""
        cls.db_path = config["testing"].DATABASE_PATH
        cls.db = get_db(cls.db_path)
        cls.db.init_db()

    def setUp(self):
        """Clear users table before each test."""
        self.db.execute("DELETE FROM users;")

    def test_password_hashing(self):
        """Test PBKDF2 password hashing and verification."""
        password = "SecurePassword123!"
        hashed = User.hash_password(password)
        
        self.assertTrue(hashed.startswith("pbkdf2:sha256:"))
        self.assertNotEqual(password, hashed)
        
        user = User(email="test@example.com", password_hash=hashed)
        self.assertTrue(user.check_password("SecurePassword123!"))
        self.assertFalse(user.check_password("WrongPassword123!"))

    def test_user_creation_and_retrieval(self):
        """Test user record creation and database retrieval."""
        user = User.create(
            email="designer.sarah@dreamhome.com",
            password="Designer123!Password",
            full_name="Sarah Jenkins",
            role="Designer",
            company="Studio Jenkins",
            phone="+1-555-0192"
        )

        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, "designer.sarah@dreamhome.com")
        self.assertEqual(user.role, "Designer")
        self.assertTrue(user.is_active)

        fetched = User.get_by_id(user.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.full_name, "Sarah Jenkins")

        by_email = User.get_by_email("DESIGNER.SARAH@DREAMHOME.COM")
        self.assertIsNotNone(by_email)
        self.assertEqual(by_email.id, user.id)

    def test_role_filtering(self):
        """Test user query filtering by role."""
        User.create("admin@dreamhome.com", "Pass123!", "Admin User", "Admin")
        User.create("designer1@dreamhome.com", "Pass123!", "Designer 1", "Designer")
        User.create("designer2@dreamhome.com", "Pass123!", "Designer 2", "Designer")
        User.create("client1@dreamhome.com", "Pass123!", "Client 1", "Client")

        designers = User.get_all(role="Designer")
        self.assertEqual(len(designers), 2)
        
        clients = User.get_all(role="Client")
        self.assertEqual(len(clients), 1)

    def test_user_update_and_deactivation(self):
        """Test updating profile attributes and account deactivation."""
        user = User.create("update.test@example.com", "Pass123!", "Initial Name", "Client")
        
        updated = user.update(full_name="Updated Name", phone="+1-800-0000")
        self.assertEqual(updated.full_name, "Updated Name")
        self.assertEqual(updated.phone, "+1-800-0000")

        # Test deactivation
        user.delete()
        deactivated = User.get_by_id(user.id)
        self.assertFalse(deactivated.is_active)

if __name__ == "__main__":
    unittest.main()
