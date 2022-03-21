import pytest
from fastapi.testclient import TestClient

from app.database import Base, DatabaseSetup, db_version, get_session
from app.main import app

db_version = DatabaseSetup.dev_database()

Base.metadata.drop_all(bind=db_version.engine)
Base.metadata.create_all(bind=db_version.engine)

client = TestClient(app)


def override_get_db():
    try:
        db = db_version.SessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = override_get_db


class TestTask:
    @pytest.fixture(autouse=True)
    def init(self):
        self.user_create = client.post("/user", json={"hashed_password": "string", "is_active": True})
        self.user_data = self.user_create.json()

    @pytest.fixture()
    def test_db(self):
        Base.metadata.create_all(bind=db_version.engine)
        yield
        Base.metadata.drop_all(bind=db_version.engine)
        Base.metadata.create_all(bind=db_version.engine)

    @pytest.fixture()
    def create_task(self):
        self.task_create = client.post(
            "/task",
            json={"name": "string", "creator_id": self.user_data["id"]},
        )
        self.task_data = self.task_create.json()

    def test_create_task_ok(self, test_db):
        task = {"name": "string3", "creator_id": self.user_data["id"]}

        response = client.post(
            "/task",
            json=task,
        )
        data = response.json()
        assert response.status_code == 201, response.text
        assert data["name"] == "string3"
        assert data["creator_id"] == self.user_data["id"]

    def test_read_task_ok(self, test_db, create_task):
        response = client.get(f'/task/{self.task_data["id"]}')
        data = response.json()

        assert response.status_code == 200, response.text

    def test_read_tasks_ok(self, test_db):
        response = client.get(f"/task")
        assert response.status_code == 200, response.text

    def test_upadte_task_ok(self, test_db, create_task):

        task_update = {"name": "string_update", "completed": True}
        response = client.put(
            f'/task/{self.task_data["id"]}',
            params=task_update,
        )
        data = response.json()

        assert response.status_code == 200, response.text
        assert data["name"] == "string_update"
        assert data["creator_id"] == self.user_data["id"]

    def test_delete_task_ok(self, test_db, create_task):
        response = client.delete(
            f'/task/{self.task_data["id"]}',
        )

        assert response.status_code == 204, response.text
