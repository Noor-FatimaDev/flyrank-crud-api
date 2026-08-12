from fastapi import FastAPI

app = FastAPI()

tasks = [
        {"id": "1", "title": "Task 1", "done": False},
        {"id": "2", "title": "Task 2", "done": False},
        {"id": "3", "title": "Task 3", "done": False}
        ]
 
@app.get("/")
def read_something():
    return {"message": "Hello, World!"}

@app.get("/health")
def check_health():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/health", "/tasks"]}

@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{id}")
def get_task(id: str):
    for task in tasks:
        if task["id"] == id:
            return task
    return {"error": "Task not found"}