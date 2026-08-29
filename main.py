from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
from database import get_all_tasks, get_task_by_id, init_db, insert_task, update_task as db_update_task, delete_task as db_delete_task

class Create_task(BaseModel):
    title: str
    done: bool=False

class Task(BaseModel):
    id: str
    title: str
    done: bool=False

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
 
@app.get("/")
def read_something():
    return {"message": "Hello, World!"}

@app.get("/health")
def check_health():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/health", "/tasks"]}

@app.get("/tasks")
def get_tasks():
    return get_all_tasks()

@app.get("/tasks/{id}")
def get_task(id: str):
    task = get_task_by_id(id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", status_code=201)
def create_task(task: Create_task):
    if task.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    new_task = insert_task(task.title, task.done)
    return {"message": "Created", "task": new_task}

@app.put("/tasks/{id}")
def update_task(id: str, task: Create_task):
    if task.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    success = db_update_task(id, task.title, task.done)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
        
    return {"message": "Updated", "task": Task(id=id, title=task.title, done=task.done)}

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: str):
    success = db_delete_task(id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None