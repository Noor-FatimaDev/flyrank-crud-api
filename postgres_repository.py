import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from models import Task

load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")

def get_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                       (id SERIAL PRIMARY KEY,
                        title TEXT NOT NULL,
                        done BOOLEAN DEFAULT FALSE)''')
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return [Task(id=str(row["id"]), title=row["title"], done=row["done"]) for row in rows]

def get_task_by_id(id: str):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    return Task(id=str(row["id"]), title=row["title"], done=row["done"])

def insert_task(title: str, done: bool):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id", (title, done))
    new_id = cursor.fetchone()["id"]
    conn.commit()
    conn.close()
    return Task(id=str(new_id), title=title, done=done)

def update_task(id: str, title: str, done: bool):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("UPDATE tasks SET title = %s, done = %s WHERE id = %s", (title, done, id))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def delete_task(id: str):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0