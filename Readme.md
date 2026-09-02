# Building CRUD API

A simple CRUD API for managing tasks, built with FastAPI as part of a Backend AI Engineering assignment at FlyRank AI. Supports creating, reading, updating, and deleting tasks. Originally built on SQLite; as of Assignment 3, the storage layer was replaced with PostgreSQL, and the whole app (API + database) now runs containerized via Docker Compose.

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Pydantic
- PostgreSQL (current storage)
- psycopg2
- Docker & Docker Compose
- SQLite (used in Assignment 2; kept in the repo for reference, no longer used at runtime)

## Setup (Docker - recommended)

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your own values (a database user, password, and db name of your choice)
3. Run:

docker compose up --build

4. This starts both the Postgres database and the API together. On first run, `schema.sql` automatically creates the `tasks` table inside the database container.
5. The API will be running at `http://localhost:8000`

## Setup (without Docker — alternative)

1. Clone the repository
2. Create and activate a virtual environment:

python -m venv venv
venv\Scripts\Activate.ps1   # Windows
source venv/bin/activate    # Mac/Linux

3. Install dependencies:

pip install -r requirements.txt

4. Make sure a Postgres server is running and reachable, and that `.env` points to it
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

## Database

This project now uses PostgreSQL, running as its own service inside Docker Compose, instead of the SQLite file used in Assignment 2. The connection string lives in `.env` (gitignored; see `.env.example` for the required shape), and the table schema is defined in `schema.sql`.

Swapping the storage layer required no changes to the API routes or service logic — both the SQLite (`database.py`) and Postgres (`postgres_repository.py`) implementations expose the exact same function signatures, so `main.py` only needed a one-line import change to switch between them.

Postgres's data is stored in a Docker volume (`pgdata`), separate from the container itself. This means data survives a container restart or teardown. I verified this directly: created a task through the API, ran `docker compose down` (which stops and removes both containers), then `docker compose up --build` again — the task was still present in `GET /tasks` afterward.

### Example SQL query

```sql
SELECT * FROM tasks WHERE done = true;
```

![Database Screenshot](screenshots/database.png)