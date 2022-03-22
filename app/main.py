from fastapi import FastAPI

from app.database import Base, engine
from app.endpoints import router

Base.metadata.create_all(engine)
app = FastAPI()

app.include_router(router)
