from pydantic import BaseModel

class TaskCreate(BaseModel):
    name: str

class Task(BaseModel):
    id: int
    name: str
    completed: bool
    class Config:
        orm_mode = True