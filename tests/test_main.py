import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.queue_manager import patients, queues, token_counters

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_in_memory_data():
    patients.clear()
    queues.clear()
    token_counters.clear()
    yield
    patients.clear()
    queues.clear()
    token_counters.clear()


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_list_doctors():
    response = client.get("/doctors")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_register_patient_and_check_token():
    response = client.post(
        "/patients",
        json={"name": "Asha", "age": 24, "doctor_id": 1},
    )
    assert response.status_code == 201
    token = response.json()["token"]
    assert token == "1-001"

    token_response = client.get(f"/token/{token}")
    assert token_response.status_code == 200
    assert token_response.json()["name"] == "Asha"


def test_invalid_doctor_is_rejected():
    response = client.post(
        "/patients",
        json={"name": "Asha", "age": 24, "doctor_id": 999},
    )
    assert response.status_code == 404


def test_call_next_patient_updates_status():
    created = client.post(
        "/patients",
        json={"name": "Ravi", "age": 35, "doctor_id": 2},
    )
    token = created.json()["token"]

    called = client.put("/queue/next/2")
    assert called.status_code == 200
    assert called.json()["patient"]["token"] == token
    assert client.get(f"/token/{token}").json()["status"] == "In Consultation"
