"""
DreamHome Studio — Database Manager
Provides SQLite thread-safe database connection management, query execution helpers,
transaction handling, schema initialization, and migration support.
"""

import sqlite3
import os
from pathlib import Path
from contextlib import contextmanager
from typing import List, Dict, Any, Optional, Tuple

class DatabaseManager:
    """Manages SQLite database connections and operations."""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            from config import Config
            db_path = Config.DATABASE_PATH
        self.db_path = db_path
        # Ensure parent directory exists
        os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        """Create and configure a sqlite3 Connection with row factory."""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        return conn

    @contextmanager
    def transaction(self):
        """Context manager for atomic database transactions."""
        conn = self.get_connection()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def execute_script(self, script_text: str) -> None:
        """Execute a raw SQL script (e.g. schema definitions)."""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(script_text)

    def init_db(self, schema_file_path: Optional[str] = None) -> None:
        """Initialize database with full schema definition if tables do not exist."""
        if schema_file_path is None:
            schema_file_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        
        with open(schema_file_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()
            
        self.execute_script(schema_sql)

    def query_all(self, query: str, params: Tuple = ()) -> List[Dict[str, Any]]:
        """Execute SELECT query and return list of dictionaries."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def query_one(self, query: str, params: Tuple = ()) -> Optional[Dict[str, Any]]:
        """Execute SELECT query and return a single row as dictionary or None."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None

    def execute(self, query: str, params: Tuple = ()) -> int:
        """Execute INSERT, UPDATE, or DELETE query and return lastrowid or rowcount."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid if cursor.lastrowid else cursor.rowcount

    def execute_many(self, query: str, params_list: List[Tuple]) -> int:
        """Execute bulk parameter query."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            return cursor.rowcount

    def count(self, table_name: str, where_clause: str = "1=1", params: Tuple = ()) -> int:
        """Count rows in a table matching condition."""
        query = f"SELECT COUNT(*) as cnt FROM {table_name} WHERE {where_clause};"
        result = self.query_one(query, params)
        return result["cnt"] if result else 0

# Global singleton instance helper
_db_instance: Optional[DatabaseManager] = None

def get_db(db_path: Optional[str] = None) -> DatabaseManager:
    """Retrieve database manager instance, respecting Flask app context config if active."""
    global _db_instance
    
    # Try fetching database path from Flask app context if available
    try:
        from flask import current_app, has_app_context
        if has_app_context() and current_app and "DATABASE_PATH" in current_app.config:
            db_path = current_app.config["DATABASE_PATH"]
    except Exception:
        pass
        
    if _db_instance is None or (db_path and _db_instance.db_path != db_path):
        _db_instance = DatabaseManager(db_path)
    return _db_instance
