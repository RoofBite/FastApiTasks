from starlette.config import Config

config = Config(".env")
PROJECT_NAME = config("FastApiTasks", default="FastAPI application")
DEBUG = config("DEBUG", cast=bool, default=False)
