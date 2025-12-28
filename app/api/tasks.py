from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.task_service import get_tasks, create_task, get_task, update_task, delete_task, update_task_status
from app.schemas.task import TaskResponse, TaskCreate, TaskUpdate, TaskStatus, TaskPriority, TaskStatusUpdate
from typing import Optional
from enum import Enum

class SortBy(str, Enum):
    ID = "id"
    TITLE = "title"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    PRIORITY = "priority"
    STATUS = "status"
    ASSIGNEE = "assignee"

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=list[TaskResponse])
def read_tasks(
    status: Optional[TaskStatus] = Query(None, description="Filter by status"),
    assignee: Optional[str] = Query(None, description="Filter by assignee"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by priority"),
    sort_by: Optional[SortBy] = Query(None, description="Sort by field"),
    sort_order: Optional[SortOrder] = Query(SortOrder.ASC, description="Sort order (asc/desc)"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    tasks = get_tasks(
        db, 
        status=status.value if status else None, 
        assignee=assignee, 
        priority=priority.value if priority else None,
        sort_by=sort_by.value if sort_by else None,
        sort_order=sort_order.value if sort_order else None,
        skip=skip,
        limit=limit
    )
    return tasks

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task_endpoint(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task)

@router.get("/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task_endpoint(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = update_task(db, task_id, task_update)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status_endpoint(task_id: int, status_update: TaskStatusUpdate, db: Session = Depends(get_db)):
    task = update_task_status(db, task_id, status_update.status)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}", status_code=204)
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    success = delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None