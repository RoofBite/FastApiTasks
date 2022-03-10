from fastapi import FastAPI

from app.endpoints import router

app = FastAPI()

app.include_router(router)
