"""
DreamHome Studio — Project Timeline & Critical Path Service
Generates milestone schedules, Gantt chart data structures, and task dependencies.
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from backend.models.task import Task

class ProjectTimelineService:
    """Project scheduling and milestone timeline generator."""

    @classmethod
    def generate_gantt_data(cls, project_id: int) -> Dict[str, Any]:
        """
        Build Gantt chart dataset for all tasks in a project.
        """
        tasks = Task.get_by_project_id(project_id)
        
        milestones = []
        total_estimated_hours = 0.0

        for t in tasks:
            total_estimated_hours += t.estimated_hours
            milestones.append({
                "task_id": t.id,
                "title": t.title,
                "assigned_to": t.assigned_name or "Unassigned",
                "status": t.status,
                "priority": t.priority,
                "due_date": t.due_date,
                "estimated_hours": t.estimated_hours,
                "is_completed": t.status == "Completed"
            })

        return {
            "project_id": project_id,
            "total_tasks": len(tasks),
            "total_estimated_hours": round(total_estimated_hours, 1),
            "milestones": milestones
        }
