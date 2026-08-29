from pydantic import BaseModel
from models import Task
import sqlite3

data_base= "tasks.db"

def get_connection():
    
   conn = sqlite3.connect(data_base)
   conn.row_factory = sqlite3.Row
   return conn

def init_db():
   conn = get_connection()
   conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                     (id INTEGER PRIMARY KEY ,
                      title TEXT NOT NULL,
                      done INTEGER default 0)''')
   
   cursor = conn.execute("SELECT COUNT(*) FROM tasks")
   count = cursor.fetchone()[0]
   
   if count == 0:
      conn.executemany('''INSERT INTO tasks (title, done) VALUES (?,?)''',
                       [
         ("Buy milk", 0),
        ("Walk dog", 0),
        ("Finish assignment", 1)
                       ]
                         )
   conn.commit()
   conn.close()

def get_all_tasks():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return [Task(id=str(row["id"]), title=row["title"], done=bool(row["done"])) for row in rows]

def get_task_by_id(id: str):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (id,)).fetchone()
    conn.close()
    if row is None:
        return None
    return Task(id=str(row["id"]), title=row["title"], done=bool(row["done"]))

def insert_task(title: str, done: bool):
    conn = get_connection()
    cursor = conn.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (title, done))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return Task(id=str(new_id), title=title, done=done)

def update_task(id: str, title: str, done: bool):
    conn = get_connection()
    cursor = conn.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (title, done, id))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def delete_task(id: str):
    conn = get_connection()
    cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0