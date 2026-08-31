"""
DreamHome Studio — User Data Model
Handles user persistence, password hashing, role checks, and user query operations.
"""

import hashlib
import os
from typing import Optional, List, Dict, Any
from database.db_manager import get_db

class User:
    """User entity model."""

    def __init__(
        self,
        id: Optional[int] = None,
        email: str = "",
        password_hash: str = "",
        full_name: str = "",
        role: str = "Client",
        avatar_url: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        bio: Optional[str] = None,
        is_active: bool = True,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
    ):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.full_name = full_name
        self.role = role
        self.avatar_url = avatar_url or "/static/images/avatars/default.jpg"
        self.phone = phone
        self.company = company
        self.bio = bio
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash plain text password with PBKDF2 HMAC SHA-256."""
        salt = "dh_studio_salt_983741"
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return f"pbkdf2:sha256:100000${salt}${key.hex()}"

    def check_password(self, password: str) -> bool:
        """Verify plain text password against stored hash."""
        return self.password_hash == User.hash_password(password)

    def to_dict(self, include_private: bool = False) -> Dict[str, Any]:
        """Serialize user object to dictionary."""
        data = {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "role": self.role,
            "avatar_url": self.avatar_url,
            "phone": self.phone,
            "company": self.company,
            "bio": self.bio,
            "is_active": bool(self.is_active),
            "created_at": str(self.created_at) if self.created_at else None,
            "updated_at": str(self.updated_at) if self.updated_at else None
        }
        if include_private:
            data["password_hash"] = self.password_hash
        return data

    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> "User":
        """Construct User instance from SQLite database row dictionary."""
        return cls(
            id=row["id"],
            email=row["email"],
            password_hash=row["password_hash"],
            full_name=row["full_name"],
            role=row["role"],
            avatar_url=row.get("avatar_url"),
            phone=row.get("phone"),
            company=row.get("company"),
            bio=row.get("bio"),
            is_active=bool(row.get("is_active", 1)),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at")
        )

    @classmethod
    def get_by_id(cls, user_id: int) -> Optional["User"]:
        """Retrieve user by primary key ID."""
        row = get_db().query_one("SELECT * FROM users WHERE id = ?;", (user_id,))
        return cls.from_row(row) if row else None

    @classmethod
    def get_by_email(cls, email: str) -> Optional["User"]:
        """Retrieve user by unique email address."""
        row = get_db().query_one("SELECT * FROM users WHERE LOWER(email) = LOWER(?);", (email.strip(),))
        return cls.from_row(row) if row else None

    @classmethod
    def get_all(cls, role: Optional[str] = None, active_only: bool = True) -> List["User"]:
        """Retrieve list of users with optional role filtering."""
        query = "SELECT * FROM users WHERE 1=1"
        params = []
        if active_only:
            query += " AND is_active = 1"
        if role:
            query += " AND role = ?"
            params.append(role)
        query += " ORDER BY id DESC;"
        
        rows = get_db().query_all(query, tuple(params))
        return [cls.from_row(r) for r in rows]

    @classmethod
    def create(
        cls,
        email: str,
        password: str,
        full_name: str,
        role: str = "Client",
        phone: Optional[str] = None,
        company: Optional[str] = None,
        bio: Optional[str] = None
    ) -> "User":
        """Create and persist new user in database."""
        password_hash = cls.hash_password(password)
        db = get_db()
        user_id = db.execute(
            """INSERT INTO users (email, password_hash, full_name, role, phone, company, bio) 
               VALUES (?, ?, ?, ?, ?, ?, ?);""",
            (email.strip().lower(), password_hash, full_name.strip(), role, phone, company, bio)
        )
        return cls.get_by_id(user_id)

    def update(self, **kwargs) -> "User":
        """Update instance attributes and persist changes to database."""
        allowed_fields = {"email", "full_name", "role", "avatar_url", "phone", "company", "bio", "is_active"}
        updates = []
        params = []
        
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(self, key, value)
                updates.append(f"{key} = ?")
                params.append(value)
                
        if "password" in kwargs and kwargs["password"]:
            self.password_hash = self.hash_password(kwargs["password"])
            updates.append("password_hash = ?")
            params.append(self.password_hash)
            
        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            params.append(self.id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?;"
            get_db().execute(query, tuple(params))
            
        return User.get_by_id(self.id)

    def delete(self) -> bool:
        """Deactivate or delete user."""
        db = get_db()
        count = db.execute("UPDATE users SET is_active = 0 WHERE id = ?;", (self.id,))
        return count > 0
