from fastapi import FastAPI

from app.config import DEBUG, PROJECT_NAME
from app.database import Base, engine
from app.endpoints import router
import uvicorn

def get_application() -> FastAPI:
    # Creates database on aplication start
    Base.metadata.create_all(engine)

    application = FastAPI(title=PROJECT_NAME, debug=DEBUG)

    application.include_router(router)

    return application


app = get_application()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)