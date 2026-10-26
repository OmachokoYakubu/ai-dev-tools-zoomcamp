import pytest
from fastapi.testclient import TestClient
from incident_response.responder import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_responder_health(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_synthetic_alert_handling(client):
    payload = {
        "version": "4",
        "status": "firing",
        "alerts": [
            {
                "status": "firing",
                "labels": {
                    "alertname": "ResponderTest",
                    "test": "true",
                    "severity": "info",
                },
                "annotations": {
                    "summary": "Synthetic test ping",
                },
            }
        ],
    }
    response = client.post("/alerts", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["processed"] == 1
    assert data["results"][0]["action"] == "verified_synthetic_test"
    assert "no incident to fix" in data["results"][0]["summary"].lower()


def test_high_error_rate_alert_handling(client):
    payload = {
        "version": "4",
        "status": "firing",
        "alerts": [
            {
                "status": "firing",
                "labels": {
                    "alertname": "HighErrorRate5xx",
                    "severity": "critical",
                    "path": "/api/orders/express-1002",
                },
                "annotations": {
                    "summary": "Elevated 5xx error rate",
                },
            }
        ],
    }
    response = client.post("/alerts", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["processed"] == 1
    assert data["results"][0]["status"] == "remediated"
    assert data["results"][0]["action"] == "remediation_applied"
