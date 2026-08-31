"""
DreamHome Studio — Notification Engine & Event Dispatcher Service
Dispatches real-time alerts and user notifications for comments, approvals, and stock warnings.
"""

from typing import Optional, Dict, Any
from backend.models.notification import Notification

class NotificationEngineService:
    """Centralized notification dispatch service."""

    @staticmethod
    def notify_approval_requested(client_id: int, project_title: str, floorplan_id: int) -> Notification:
        """Notify client when designer submits a floorplan for formal approval."""
        return Notification.create(
            user_id=client_id,
            title="Design Approval Requested",
            message=f"Designer has submitted a new floorplan layout for '{project_title}' for your review.",
            type="Approval",
            target_url=f"/projects/floorplans/{floorplan_id}"
        )

    @staticmethod
    def notify_comment_posted(designer_id: int, commenter_name: str, floorplan_name: str) -> Notification:
        """Notify designer when a new comment is posted on a floorplan."""
        return Notification.create(
            user_id=designer_id,
            title="New Floorplan Comment",
            message=f"{commenter_name} added a feedback pin on '{floorplan_name}'.",
            type="Info",
            target_url="/collaboration"
        )
