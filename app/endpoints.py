from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.models as models
import app.schemas as schemas
from app.database import SessionLocal
from app.exceptions import ITEM_NOT_FOUND, USER_NOT_FOUND

router = APIRouter()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.post("/user", response_model=schemas.UserCreateOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, session: Session = Depends(get_session)):
    userdb = models.User(is_active=user.is_active, hashed_password=user.hashed_password)
    session.add(userdb)
    session.commit()
    session.refresh(userdb)

    return userdb


@router.get("/search/", response_model=List[schemas.Task], status_code=status.HTTP_200_OK)
def search(name=str, session: Session = Depends(get_session)):
    name_query = session.query(models.Task).filter(models.Task.name == name).all()

    return name_query


@router.post("/task", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, session: Session = Depends(get_session)):
    taskdb = models.Task(name=task.name, creator_id=task.creator_id)

    if session.query(models.User).filter(models.User.id == task.creator_id).first():
        taskdb.creator_id = task.creator_id
    else:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND.format(id=str(id)))

    taskdb.completed = False

    session.add(taskdb)
    session.commit()
    session.refresh(taskdb)

    return taskdb


@router.get("/task/{id}", response_model=schemas.Task)
def read_task(id: int, session: Session = Depends(get_session)):
    task = session.query(models.Task).get(id)

    if not task:
        raise HTTPException(status_code=404, detail=ITEM_NOT_FOUND.format(id=str(id)))

    return task


@router.put("/task/{id}", response_model=schemas.Task)
def update_task(id: int, name: str, completed: bool, session: Session = Depends(get_session)):
    task = session.query(models.Task).get(id)

    if task:
        task.name = name
        task.completed = completed
        session.commit()

    if not task:
        raise HTTPException(status_code=404, detail=ITEM_NOT_FOUND.format(id=str(id)))

    return task


@router.delete("/task/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, session: Session = Depends(get_session)):
    task = session.query(models.Task).get(id)
    if task:
        session.delete(task)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=ITEM_NOT_FOUND.format(id=str(id)))

    return None


@router.get("/task", response_model=List[schemas.Task])
def read_task_list(session: Session = Depends(get_session)):
    task_list = session.query(models.Task).all()

    return task_list
