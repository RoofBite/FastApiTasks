import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestSearch:
    @pytest.fixture()
    def create_user(self):
        self.user_create = client.post("/user", json={"hashed_password": "string", "is_active": True})
        self.user_data = self.user_create.json()

    @pytest.fixture()
    def create_task(self, create_user):
        self.task_create = client.post(
            "/task",
            json={"name": "Learn TDD", "creator_id": self.user_data["id"]},
        )
        self.task_data = self.task_create.json()
        self.task_create3 = client.post(
            "/task",
            json={"name": "Learn TDDX", "creator_id": self.user_data["id"]},
        )
        self.task_data3 = self.task_create3.json()
        self.task_create4 = client.post(
            "/task",
            json={"name": "Learn TDDX", "creator_id": self.user_data["id"]},
        )
        self.task_data4 = self.task_create4.json()
        self.task_create2 = client.post(
            "/task",
            json={"name": "Learn", "creator_id": self.user_data["id"]},
        )
        self.task_data2 = self.task_create2.json()

    def test_get_search_with_no_data(self):
        pass
        # response = client.get("/search")
        # assert response.status_code == 200
        # assert response.json() == []

    def test_get_tasks_with_name(self, db_session, create_task):
        name = "Learn TDD"
        response = client.get(f"/search/?name={name}")
        assert response.status_code == 200
        assert response.json() == [self.task_data]

    def test_get_all_tasks_with_name_not_completed(self, db_session, create_task):
        name = "Learn TDDX"
        response = client.get(f"/search/?name={name}&partial={False}")
        assert response.status_code == 200

        assert response.json() == [self.task_data3, self.task_data4]

    def test_get_tasks_with_partial_name(self, db_session, create_task):
        name = "Learn"
        # we have Learn and Learn TDD tasks
        response = client.get(f"/search/?name={name}&partial={True}")

        assert response.status_code == 200
        assert response.json() == [self.task_data, self.task_data3, self.task_data4, self.task_data2]

    def test_get_all_tasks_with_name(self, db_session, create_task):
        name = "Learn TDDX"
        response = client.get(f"/search/?name={name}")
        assert response.status_code == 200

        assert response.json() == [self.task_data3, self.task_data4]

    def test_get_tasks_with_partial_name_not_completed(self, db_session, create_task):
        name = "Learn"
        # we have Learn and Learn TDD tasks
        response = client.get(f"/search/?name={name}&partial={False}")

        assert response.status_code == 200
        assert response.json() == [self.task_data, self.task_data3, self.task_data4, self.task_data2]

    # def test_class(self):
    #     c = QueryClass()
    #     assert c.get_similar_tasks("Learn TDD") == [self.task_data]
