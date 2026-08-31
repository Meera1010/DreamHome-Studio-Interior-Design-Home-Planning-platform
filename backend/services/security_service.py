"""
DreamHome Studio — Security Service
Provides authentication token generation, password strength checks, input sanitization,
and CSRF verification routines.
"""

import secrets
import re
from typing import Optional, Dict, Any

class SecurityService:
    """Application security helper service."""

    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Generate a cryptographically secure random token string."""
        return secrets.token_hex(length)

    @staticmethod
    def sanitize_input(text: Optional[str]) -> str:
        """Sanitize plain text input against XSS injection."""
        if not text:
            return ""
        sanitized = text.replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#x27;")
        return sanitized.strip()

    @staticmethod
    def validate_password_strength(password: str) -> bool:
        """Validate password policy: minimum 8 characters."""
        if not password or len(password) < 8:
            return False
        return True

    @staticmethod
    def validate_email_format(email: str) -> bool:
        """Validate email format using standard regular expression."""
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return bool(re.match(pattern, email.strip()))
