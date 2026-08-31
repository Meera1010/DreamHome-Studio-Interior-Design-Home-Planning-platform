"""
DreamHome Studio — Authentication & User REST API
Endpoints for user registration, authentication, logout, profile view/update, and password management.
"""

from flask import Blueprint, request, jsonify, session
from backend.models.user import User
from backend.models.audit_log import AuditLog
from backend.auth.security import login_required, get_current_user
from backend.utils.validators import validate_required_fields

auth_bp = Blueprint("auth_api", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user account."""
    data = request.get_json() or {}
    valid, err = validate_required_fields(data, ["email", "password", "full_name"])
    if not valid:
        return jsonify({"error": err}), 400

    email = data["email"].strip().lower()
    if User.get_by_email(email):
        return jsonify({"error": "An account with this email already exists"}), 409

    role = data.get("role", "Client")
    if role not in ("Designer", "Client", "Admin"):
        role = "Client"

    user = User.create(
        email=email,
        password=data["password"],
        full_name=data["full_name"],
        role=role,
        phone=data.get("phone"),
        company=data.get("company"),
        bio=data.get("bio")
    )

    session["user_id"] = user.id
    session["role"] = user.role
    session["user_name"] = user.full_name

    AuditLog.log("USER_REGISTER", "User", user.id, user.id, {"email": user.email, "role": user.role})
    return jsonify({"message": "Registration successful", "user": user.to_dict()}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate user and initialize HTTP session."""
    data = request.get_json() or {}
    valid, err = validate_required_fields(data, ["email", "password"])
    if not valid:
        return jsonify({"error": err}), 400

    email = data["email"].strip().lower()
    user = User.get_by_email(email)

    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    if not user.is_active:
        return jsonify({"error": "Account is deactivated"}), 403

    session["user_id"] = user.id
    session["role"] = user.role
    session["user_name"] = user.full_name

    AuditLog.log("USER_LOGIN", "User", user.id, user.id, {"email": user.email})
    return jsonify({"message": "Login successful", "user": user.to_dict()}), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Clear session data."""
    user_id = session.get("user_id")
    if user_id:
        AuditLog.log("USER_LOGOUT", "User", user_id, user_id)
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

@auth_bp.route("/me", methods=["GET"])

def get_current_profile():
    """Return currently authenticated user profile or null."""
    if "user_id" not in session:
        return jsonify({"authenticated": False, "user": None}), 200
    user = get_current_user()
    if not user or not user.is_active:
        session.clear()
        return jsonify({"authenticated": False, "user": None}), 200
    return jsonify({"authenticated": True, "user": user.to_dict()}), 200

@auth_bp.route("/profile", methods=["PUT"])
@login_required
def update_profile():
    """Update current user profile info."""
    user = get_current_user()
    data = request.get_json() or {}
    updated_user = user.update(**data)
    session["user_name"] = updated_user.full_name
    AuditLog.log("PROFILE_UPDATE", "User", user.id, user.id)
    return jsonify({"message": "Profile updated successfully", "user": updated_user.to_dict()}), 200
