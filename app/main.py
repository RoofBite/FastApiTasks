from fastapi import FastAPI

from app.config import DEBUG, PROJECT_NAME
from app.database import Base, engine
from app.endpoints import router

# Creates database on aplication start
Base.metadata.create_all(engine)


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG)

    application.include_router(router)

    return application


app = get_application()
