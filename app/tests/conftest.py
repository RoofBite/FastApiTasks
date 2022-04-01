from urllib.parse import urlencode

import pytest
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import scoped_session, sessionmaker

from app import config as app_config
from app.database import Base


@pytest.fixture(autouse=True, scope="session")
def database(request):
    uri = make_url(app_config.DATABASE_URL)
    db_name: str = uri.database
    if not db_name.endswith("_test"):
        db_name = f"{db_name}_test"

    _app_engine = create_engine(app_config.DATABASE_URL, isolation_level="AUTOCOMMIT")
    conn = _app_engine.connect()
    try:
        conn.execute(f"CREATE DATABASE {db_name}")
    except sqlalchemy.exc.ProgrammingError:
        pass
    query = urlencode(uri.query)
    sqlalchemy_database_uri = (
        f"{uri.drivername}://{uri.username}:{uri.password}@{uri.host}:{uri.port}/{db_name}?{query}"
    )
    app_config.DATABASE_URL = sqlalchemy_database_uri
    engine = create_engine(sqlalchemy_database_uri, pool_pre_ping=True)

    yield engine

    engine.dispose()
    conn.execute(f"DROP DATABASE IF EXISTS {db_name}")


@pytest.fixture()
def db_session(database):
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=database))
    Base.metadata.create_all(database)
    yield session
    session.close()
    Base.metadata.drop_all(database)


@pytest.fixture(autouse=True)
def mock_local_session(monkeypatch, database):
    monkeypatch.setattr(
        "app.endpoints.SessionLocal",
        sessionmaker(autocommit=False, autoflush=False, bind=database),
    )
