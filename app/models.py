from xmlrpc.client import Boolean
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    tasks = relationship("Task", back_populates="creator")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    completed = Column(Boolean)
    creator_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="tasks")
