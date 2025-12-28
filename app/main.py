from fastapi import FastAPI
from app.api.tasks import router as tasks_router

app = FastAPI(title="Task Tracker API", version="1.0.0")

app.include_router(tasks_router)

@app.get("/")
def read_root():
    return {"message": "Task Tracker API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}