import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestTask:
    @pytest.fixture()
    def create_user(self):
        self.user_create = client.post("/user", json={"hashed_password": "string", "is_active": True})
        self.user_data = self.user_create.json()

    @pytest.fixture()
    def create_task(self, create_user):
        self.task_create = client.post(
            "/task",
            json={"name": "string", "creator_id": self.user_data["id"]},
        )
        self.task_data = self.task_create.json()

    def test_create_task_ok(self, db_session, create_user):
        self.user_create = client.post("/user", json={"hashed_password": "string", "is_active": True})
        self.user_data = self.user_create.json()
        task = {"name": "string3", "creator_id": self.user_data["id"]}

        response = client.post(
            "/task",
            json=task,
        )
        data = response.json()
        assert response.status_code == 201, response.text
        assert data["name"] == "string3"
        assert data["creator_id"] == self.user_data["id"]

    def test_read_task_ok(self, db_session, create_task):
        response = client.get(f'/task/{self.task_data["id"]}')
        data = response.json()
        assert response.status_code == 200, response.text

    def test_read_tasks_ok(self, db_session):
        response = client.get(f"/task")
        assert response.status_code == 200, response.text

    def test_upadte_task_ok(self, db_session, create_task):

        task_update = {"name": "string_update", "completed": True}
        response = client.put(
            f'/task/{self.task_data["id"]}',
            params=task_update,
        )
        data = response.json()

        assert response.status_code == 200, response.text
        assert data["name"] == "string_update"
        assert data["creator_id"] == self.user_data["id"]

    def test_delete_task_ok(self, db_session, create_task):
        response = client.delete(
            f'/task/{self.task_data["id"]}',
        )

        assert response.status_code == 204, response.text
