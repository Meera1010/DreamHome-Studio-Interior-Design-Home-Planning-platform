"""
DreamHome Studio — Notifications REST API
Endpoints for fetching user notifications and marking alerts as read.
"""

from flask import Blueprint, jsonify, session
from backend.models.notification import Notification
from backend.auth.security import login_required, get_current_user

notifications_bp = Blueprint("notifications_api", __name__, url_prefix="/api/notifications")

@notifications_bp.route("", methods=["GET"])
@login_required
def get_user_notifications():
    """Retrieve notifications for active user."""
    user = get_current_user()
    notifs = Notification.get_by_user(user.id)
    return jsonify({"notifications": [n.to_dict() for n in notifs]}), 200

@notifications_bp.route("/read-all", methods=["POST"])
@login_required
def mark_all_read():
    """Mark all user notifications as read."""
    user = get_current_user()
    Notification.mark_all_as_read(user.id)
    return jsonify({"message": "Notifications marked as read"}), 200
