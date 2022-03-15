from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_session
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = override_get_db

client = TestClient(app)


def test_create_task_ok():
    response = client.post("/user", json={"hashed_password": "string", "is_active": True})

    data = response.json()
    assert "id" in data
    task = {"name": "string", "creator_id": data["id"]}

    response = client.post(
        "/task",
        json=task,
    )
    data = response.json()
    import logging

    logging.error(data)
    assert response.status_code == 201, response.text


def test_read_task_ok():
    response = client.post("/user", json={"hashed_password": "string", "is_active": True})

    data = response.json()
    import logging

    logging.error(data)
    assert "id" in data
    response = client.get(f"/task/1")
    assert response.status_code == 200, response.text


def test_read_tasks_ok():
    client.post("/user", json={"hashed_password": "string", "is_active": True})

    response = client.get(f"/task")
    assert response.status_code == 200, response.text


def test_upadte_task_ok():
    response = client.post("/user", json={"hashed_password": "string", "is_active": True})

    data = response.json()
    assert "id" in data
    task = {"name": "string", "creator_id": data["id"]}
    client.post(
        "/task",
        json=task,
    )

    task_update = {"name": "string_update", "creator_id": data["id"]}

    response = client.put(
        "/task/1",
        json=task_update,
    )
    data = response.json()
    assert response.status_code == 204, response.text
    assert data["name"] == "string_update"
