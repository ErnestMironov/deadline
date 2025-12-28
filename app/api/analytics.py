from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.analytics_service import get_tasks_analytics, generate_tasks_chart
from app.schemas.analytics import TasksAnalyticsResponse

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/tasks", response_model=TasksAnalyticsResponse)
def get_analytics(db: Session = Depends(get_db)):
    return get_tasks_analytics(db)

@router.get("/tasks/chart")
def get_tasks_chart(db: Session = Depends(get_db)):
    img_buf = generate_tasks_chart(db)
    return Response(content=img_buf.getvalue(), media_type="image/png")