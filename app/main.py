from typing import List

from exceptions import ITEM_NOT_FOUND
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

import app.models as models
import app.schemas as schemas
from app.database import Base, SessionLocal, engine
from app.exceptions import ITEM_NOT_FOUND

Base.metadata.create_all(engine)
app = FastAPI()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.post("/task", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, session: Session = Depends(get_session)):
    taskdb = models.Task(name=task.name)
    taskdb.completed = False

    session.add(taskdb)
    session.commit()
    session.refresh(taskdb)

    return taskdb


@app.get("/task/{id}", response_model=schemas.Task)
def read_task(id: int, session: Session = Depends(get_session)):
    task = session.query(models.Task).get(id)

    if not task:
        raise HTTPException(status_code=404, detail=ITEM_NOT_FOUND.format(id=str(id)))

    return task


@app.put("/task/{id}", response_model=schemas.Task)
def update_task(id: int, name: str, completed: bool, session: Session = Depends(get_session)):
    task = session.query(models.Task).get(id)

    if task:
        task.name = name
        task.completed = completed
        session.commit()

    if not task:
        raise HTTPException(status_code=404, detail=ITEM_NOT_FOUND.format(id=str(id)))

    return task


@app.delete("/task/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, session: Session = Depends(get_session)):
    task = session.query(models.Task).get(id)
    if task:
        session.delete(task)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=ITEM_NOT_FOUND.format(id=str(id)))

    return None


@app.get("/task", response_model=List[schemas.Task])
def read_task_list(session: Session = Depends(get_session)):
    task_list = session.query(models.Task).all()

    return task_list
