from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: TaskStatus = Field(default=TaskStatus.NEW)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    assignee: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None

class TaskStatusUpdate(BaseModel):
    status: TaskStatus

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True