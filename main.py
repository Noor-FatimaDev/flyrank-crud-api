from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def read_something():
    return {"message": "Hello, World!"}

@app.get("/health")
def check_health():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/health", "/tasks"]}