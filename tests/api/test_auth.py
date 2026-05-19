from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_register_user():
    register_data = {
        "first_name": "John",
        "last_name": "Doe",
        "super_last_name": "Maximovich",
        "phone_number": "+79999999999",
        "password": "test_john2026",
        "email": "test@example.com",
    }
    reg_response = client.post("/bank_app/v1/welcome/registration", json=register_data)
    assert reg_response.status_code == 200
