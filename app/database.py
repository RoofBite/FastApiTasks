from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class DatabaseSetup:
    def __init__(self, SQLALCHEMY_DATABASE_URL, engine, SessionLocal):
        self.SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL
        self.engine = engine
        self.SessionLocal = SessionLocal

    @staticmethod
    def dev_database():
        SQLALCHEMY_DATABASE_URL = "postgresql://username:password@db:5432/dev_database"
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        SessionLocal = sessionmaker(bind=engine)
        return DatabaseSetup(SQLALCHEMY_DATABASE_URL, engine, SessionLocal)

    @staticmethod
    def test_database():
        SQLALCHEMY_DATABASE_URL = "postgresql://username:password@tests:5433/test_database"
        engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return DatabaseSetup(SQLALCHEMY_DATABASE_URL, engine, SessionLocal)


db_version = DatabaseSetup.dev_database()

Base = declarative_base()

Base.metadata.create_all(db_version.engine)


def get_session():
    try:
        session = db_version.SessionLocal()
        yield session
    finally:
        session.close()
