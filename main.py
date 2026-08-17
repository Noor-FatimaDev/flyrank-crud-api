from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
from database import init_db

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

tasks = [
        Task(id="1", title="Task 1", done=False),
        Task(id="2", title="Task 2", done=False),
        Task(id="3", title="Task 3", done=False)
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
        if task.id == id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks", status_code=201)
def create_task(task: Create_task):
    if task.title == "":
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    else:
        new_task = Task(id=str(max(int(t.id) for t in tasks) + 1), title=task.title, done=task.done)
        tasks.append(new_task)
        return {"message": "Created ", "task": new_task}

@app.put("/tasks/{id}")
def update_task(id: str, task: Create_task):
    for t in tasks:
        if t.id == id:
            t.title = task.title
            t.done = task.done
            return {"message": "Updated", "task": t}
    raise HTTPException(status_code=404, detail="Task not found") 

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: str):
    for t in tasks:
        if t.id == id:
            tasks.remove(t)
            return None
    raise HTTPException(status_code=404, detail="Task not found")