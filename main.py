from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
from database import get_connection, init_db

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
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    tasks = []
    
    for row in rows:
       tasks.append (Task(id=str(row["id"]), title=row["title"], done=bool(row["done"])))
       
    conn.close()
    return tasks

@app.get("/tasks/{id}")
def get_task(id: str):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (id,)).fetchone()
    
    if row:
        task = Task(id=str(row["id"]), title=row["title"], done=bool(row["done"]))
        conn.close()
        return task
    else:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks", status_code=201)
def create_task(task: Create_task):
    conn = get_connection()
    if task.title.strip() == "":
        conn.close()
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    else:
        cursor = conn.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (task.title, task.done))
        new_id = cursor.lastrowid  
        conn.commit()
        conn.close()
        return {"message": "Created", "task": Task(id=str(new_id), title=task.title, done=task.done)}

@app.put("/tasks/{id}")
def update_task(id: str, task: Create_task):
    conn = get_connection()
    
    if task.title.strip() == "":
        conn.close()
        raise HTTPException(status_code=400, detail="Title cannot be empty")
        
    cursor = conn.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (task.title, task.done, id))
    
    if cursor.rowcount == 0:
                conn.close()
                raise HTTPException(status_code=404, detail="Task not found")
            
    conn.commit()
    conn.close()
    return {"message": "Updated", "task": Task(id=id, title=task.title, done=task.done)}

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: str):
    conn = get_connection()
    cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    
    conn.commit()
    conn.close()
    return None