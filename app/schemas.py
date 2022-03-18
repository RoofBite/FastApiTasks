from pydantic import BaseModel


class UserCreate(BaseModel):
    hashed_password: str
    is_active: bool

    class Config:
        orm_mode = True


class TaskCreate(BaseModel):
    name: str
    creator_id: int

    class Config:
        arbitrary_types_allowed = True


class Task(BaseModel):
    id: int
    name: str
    completed: bool
    creator_id: int

    class Config:
        orm_mode = True
