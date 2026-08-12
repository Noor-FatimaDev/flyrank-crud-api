# Building CRUD API

A simple CRUD API for managing tasks, built with FastAPI as part of a backend engineering assignment. Supports creating, reading, updating, and deleting tasks with in-memory storage.

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Pydantic

## Setup

1. Clone the repository
2. Create a virtual environment:

python -m venv venv

3. Activate the virtual environment:
   - Windows: `venv\Scripts\Activate.ps1`
   - Mac/Linux: `source venv/bin/activate`
   
4. Install dependencies:

pip install -r requirements.txt

5. Run the server:

uvicorn main:app --reload

6. The API will be running at `http://localhost:8000`

## Endpoints

| Method | Path         | Description                   |
|--------|--------------|-------------------------------|
| GET    | /            | Hello world / basic check     |
| GET    | /health      | API status info               |
| GET    | /tasks       | List all tasks                |
| GET    | /tasks/{id}  | Get a single task by id       |
| POST   | /tasks       | Create a new task             |
| PUT    | /tasks/{id}  | Update an existing task       |
| DELETE | /tasks/{id}  | Delete a task                 |

## API Docs

Interactive Swagger documentation is available at:

http://localhost:8000/docs


![Swagger UI](screenshots/swagger-docs.png)