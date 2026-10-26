import pytest
from fastapi.testclient import TestClient
from app import main


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "DB_PATH", tmp_path / "integration_orders.db")
    with TestClient(main.app) as test_client:
        yield test_client


def test_end_to_end_order_lifecycle(client):
    """End-to-end integration test verifying the entire customer & fulfillment workflow."""
    # 1. Health check
    health_res = client.get("/healthz")
    assert health_res.status_code == 200
    assert health_res.json() == {"status": "ok"}

    # 2. Create standard order
    create_res = client.post(
        "/api/orders",
        json={"customer": "Elena Rostova", "item": "Mechanical Keyboard", "priority": "standard"},
    )
    assert create_res.status_code == 201
    order_id = create_res.json()["id"]

    # 3. Lookup order
    get_res = client.get(f"/api/orders/{order_id}")
    assert get_res.status_code == 200
    data = get_res.json()
    assert data["customer"] == "Elena Rostova"
    assert data["status"] == "received"

    # 4. Advance through lifecycle: received -> preparing -> shipped -> delivered
    for next_status in ["preparing", "shipped", "delivered"]:
        patch_res = client.patch(f"/api/orders/{order_id}", json={"status": next_status})
        assert patch_res.status_code == 200
        assert patch_res.json()["status"] == next_status

    # 5. Create express order and verify estimated delivery calculation
    express_res = client.post(
        "/api/orders",
        json={"customer": "Marcus Vance", "item": "4K Monitor", "priority": "express"},
    )
    assert express_res.status_code == 201
    exp_id = express_res.json()["id"]

    exp_get = client.get(f"/api/orders/{exp_id}")
    assert exp_get.status_code == 200
    exp_data = exp_get.json()
    assert exp_data["priority"] == "express"
    assert "estimated_delivery" in exp_data

    # 6. Verify client error isolation (404 does not crash database)
    missing_res = client.get("/api/orders/non-existent-order-9999")
    assert missing_res.status_code == 404
    assert missing_res.json()["detail"] == "Order not found"
