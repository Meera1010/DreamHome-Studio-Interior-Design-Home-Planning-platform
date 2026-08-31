"""
DreamHome Studio — Auth & Security Middleware
Provides session authentication decorators, role-based authorization checks,
session state helpers, and security response wrappers.
"""

from functools import wraps
from flask import session, jsonify, request
from backend.models.user import User

def get_current_user():
    """Retrieve logged-in User instance from active session."""
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.get_by_id(user_id)

def login_required(f):
    """Decorator requiring an active authenticated session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Authentication required", "code": "UNAUTHORIZED"}), 401
        user = get_current_user()
        if not user or not user.is_active:
            session.clear()
            return jsonify({"error": "User session invalid or deactivated", "code": "UNAUTHORIZED"}), 401
        return f(*args, **kwargs)
    return decorated_function

def role_required(*allowed_roles):
    """Decorator requiring specific role privileges (e.g. Designer, Admin)."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                return jsonify({"error": "Authentication required", "code": "UNAUTHORIZED"}), 401
            user = get_current_user()
            if not user or user.role not in allowed_roles:
                return jsonify({
                    "error": f"Access denied. Requires one of roles: {', '.join(allowed_roles)}",
                    "code": "FORBIDDEN"
                }), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
