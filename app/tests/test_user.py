from fastapi.testclient import TestClient

from app.main import app


def test_create_user_ok():
    client = TestClient(app)

    user = {"hashed_password": "string", "is_active": True}

    response = client.post(
        "/user",
        json=user,
    )
    assert response.status_code == 201, response.text
