from pydantic import BaseModel
from typing import Dict

class TasksAnalyticsResponse(BaseModel):
    total_tasks: int
    by_status: Dict[str, int]
    by_priority: Dict[str, int]
    by_assignee: Dict[str, int]
    status_percentage: Dict[str, float]
    priority_percentage: Dict[str, float]