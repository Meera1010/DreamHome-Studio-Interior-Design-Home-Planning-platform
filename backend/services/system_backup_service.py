"""
DreamHome Studio — System Backup & Database Audit Service
Provides SQLite database integrity checks, table statistics, and database backup routines.
"""

import os
import shutil
from datetime import datetime
from typing import Dict, Any
from database.db_manager import get_db

class SystemBackupService:
    """Admin system maintenance and database backup service."""

    @staticmethod
    def get_database_stats() -> Dict[str, Any]:
        """Inspect table row counts and database file size."""
        db = get_db()
        tables = [
            "users", "projects", "floorplans", "floorplan_versions",
            "furniture_catalog", "materials_catalog", "suppliers",
            "inventory_items", "budgets", "budget_line_items",
            "tasks", "moodboards", "comments", "approval_requests",
            "portfolios", "notifications", "audit_logs"
        ]

        table_counts = {}
        total_rows = 0

        for table in tables:
            cnt = db.count(table)
            table_counts[table] = cnt
            total_rows += cnt

        file_size_bytes = 0
        if os.path.exists(db.db_path):
            file_size_bytes = os.path.getsize(db.db_path)

        return {
            "database_path": db.db_path,
            "size_mb": round(file_size_bytes / (1024 * 1024), 3),
            "total_rows": total_rows,
            "table_counts": table_counts
        }

    @staticmethod
    def create_database_backup(backup_dir: str = "database/backups") -> str:
        """Create a timestamped SQLite database file backup."""
        db = get_db()
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"dreamhome_backup_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        shutil.copy2(db.db_path, backup_path)
        return backup_path
