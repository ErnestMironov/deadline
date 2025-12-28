from fastapi import FastAPI

app = FastAPI(title="Task Tracker API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Task Tracker API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}