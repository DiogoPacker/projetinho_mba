import pytest
from fastapi.testclient import TestClient
from openai import OpenAIError

from flightlab import api
from flightlab.model import load_model, train


@pytest.fixture
def client(flights, tmp_path, monkeypatch):
    train(flights, {}, tmp_path)
    monkeypatch.setattr(api, "dataset", lambda: flights)
    monkeypatch.setattr(api, "model", lambda: load_model(tmp_path))
    return TestClient(api.app)


def test_api_analytics_prediction_and_assistant(client):
    assert client.get("/health").json()["status"] == "ok"
    assert client.get("/analytics?carrier=AA").json()["flights"] == 300
    assert client.get("/analytics?carrier=ZZ").json()["flights"] == 0
    result = client.post(
        "/predict",
        json={
            "date": "2013-11-01",
            "carrier": "AA",
            "origin": "JFK",
            "dest": "LAX",
            "distance": 2475,
        },
    )
    assert result.status_code == 200
    assert 0 <= result.json()["probability"] <= 1
    assert client.post("/assistant", json={"question": "Resumo"}).status_code == 200
    assert client.get("/model").status_code == 200


def test_api_rejects_invalid_input(client):
    assert client.get("/analytics?month=13").status_code == 422
    assert client.post("/predict", json={"date": "invalid"}).status_code == 422
    assert client.post("/assistant", json={"question": " "}).status_code == 422


def test_missing_artifact_is_service_unavailable(monkeypatch):
    def missing():
        raise FileNotFoundError("Modelo ausente")

    monkeypatch.setattr(api, "model", missing)
    assert TestClient(api.app).get("/model").status_code == 503


def test_provider_error_is_sanitized(client, monkeypatch):
    def unavailable(*args, **kwargs):
        raise OpenAIError("internal provider detail")

    monkeypatch.setattr(api, "answer", unavailable)
    response = client.post("/assistant", json={"question": "Resumo", "use_llm": True})
    assert response.status_code == 502
    assert "internal provider detail" not in response.text
