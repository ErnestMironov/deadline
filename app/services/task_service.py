from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskStatus
from typing import Optional
from enum import Enum

def get_tasks(
    db: Session, 
    status: Optional[str] = None, 
    assignee: Optional[str] = None, 
    priority: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    query = db.query(Task)
    
    if status:
        query = query.filter(Task.status == status)
    if assignee:
        query = query.filter(Task.assignee == assignee)
    if priority:
        query = query.filter(Task.priority == priority)
    
    if sort_by:
        column = getattr(Task, sort_by, None)
        if column:
            if sort_order == "desc":
                query = query.order_by(desc(column))
            else:
                query = query.order_by(asc(column))
    else:
        query = query.order_by(Task.id.asc())
    
    return query.offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def create_task(db: Session, task: TaskCreate):
    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status.value,
        priority=task.priority.value,
        assignee=task.assignee
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_update: TaskUpdate):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None
    
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if isinstance(value, Enum):
            setattr(db_task, field, value.value)
        else:
            setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task_status(db: Session, task_id: int, status: TaskStatus):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None
    
    db_task.status = status.value
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    return True