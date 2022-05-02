from starlette.config import Config

config = Config(".env")
PROJECT_NAME = config("FastApiTasks", default="FastAPI application")
DEBUG = config("DEBUG", cast=bool, default=False)
DATABASE_URL = config("DATABASE_URL", default="postgresql://username:password@db:5432/dev_database")
