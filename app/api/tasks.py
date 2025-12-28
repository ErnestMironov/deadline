from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.task_service import get_tasks, create_task
from app.schemas.task import TaskResponse, TaskCreate

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=list[TaskResponse])
def read_tasks(db: Session = Depends(get_db)):
    tasks = get_tasks(db)
    return tasks

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task_endpoint(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task)