"""
DreamHome Studio — Admin & Audit Log Unit Tests
Tests admin user role modifications, account toggles, and security audit log retention.
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
from backend.models.audit_log import AuditLog

class TestAdminAudit(unittest.TestCase):
    """Test suite for Admin panel operations and Audit logs."""

    @classmethod
    def setUpClass(cls):
        cls.db_path = config["testing"].DATABASE_PATH
        cls.db = get_db(cls.db_path)
        cls.db.init_db()

    def setUp(self):
        self.db.execute("DELETE FROM audit_logs;")
        self.db.execute("DELETE FROM users;")

        self.admin = User.create("admin@test.com", "Pass123!", "Admin", "Admin")
        self.client_user = User.create("client@test.com", "Pass123!", "Client User", "Client")

    def test_role_modification(self):
        """Test admin modifying user role."""
        updated = self.client_user.update(role="Designer")
        self.assertEqual(updated.role, "Designer")

        log = AuditLog.log("ADMIN_ROLE_CHANGE", "User", self.client_user.id, self.admin.id, {"new_role": "Designer"})
        self.assertIsNotNone(log.id)

    def test_audit_logs_retrieval(self):
        """Test logging and fetching audit entries."""
        AuditLog.log("TEST_ACTION_1", "TestEntity", 101, self.admin.id)
        AuditLog.log("TEST_ACTION_2", "TestEntity", 102, self.admin.id)

        logs = AuditLog.get_recent(10)
        self.assertEqual(len(logs), 2)
        self.assertEqual(logs[0].action, "TEST_ACTION_2")

if __name__ == "__main__":
    unittest.main()
