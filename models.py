from pydantic import BaseModel

class Task(BaseModel):
    id: int
    title: str
    done: bool = False
    
class Create_task(BaseModel):
    title: str
    done: bool=False