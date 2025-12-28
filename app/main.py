from fastapi import FastAPI
from app.api.tasks import router as tasks_router
from app.api.analytics import router as analytics_router
from app.api.auth import router as auth_router

app = FastAPI(title="Task Tracker API", version="1.0.0")

app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(analytics_router)

@app.get("/")
def read_root():
    return {"message": "Task Tracker API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}