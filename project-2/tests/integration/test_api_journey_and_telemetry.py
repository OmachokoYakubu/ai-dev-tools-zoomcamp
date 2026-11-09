"""End-to-end integration tests for ShelfSync user journey & correlated telemetry."""

from __future__ import annotations

import json
from fastapi.testclient import TestClient

from backend.main import app
from backend.telemetry import IN_MEMORY_SPAN_EXPORTER, STRUCTURED_LOG_BUFFER

client = TestClient(app)


def test_full_inventory_and_restock_user_journey_with_trace_correlation() -> None:
    sensitive_email = "confidential.rep@cryomed.example"

    # 1. Register new cold-chain SKU
    create_res = client.post(
        "/api/items",
        json={
            "sku": "VAC-MRNA99",
            "name": "mRNA Booster 5-Dose Cold Vial",
            "category": "cold_chain",
            "quantity": 10,
            "reorder_threshold": 8,
            "storage_temp_c": -20.0,
            "supplier_email": sensitive_email,
        },
    )
    assert create_res.status_code == 201
    trace_id = create_res.headers.get("X-Trace-Id", "")
    assert len(trace_id) == 32 and trace_id != "0" * 32

    # Duplicate SKU returns 409 Conflict
    dup_res = client.post(
        "/api/items",
        json={
            "sku": "VAC-MRNA99",
            "name": "Duplicate",
            "category": "cold_chain",
            "quantity": 5,
            "reorder_threshold": 5,
            "storage_temp_c": 4.0,
            "supplier_email": sensitive_email,
        },
    )
    assert dup_res.status_code == 409

    # 2. Draw down 5 units -> triggers low_stock (5 <= 8)
    draw_res = client.post(
        "/api/items/VAC-MRNA99/drawdown",
        json={"units": 5, "reason": "Morning immunization clinic"},
    )
    assert draw_res.status_code == 200
    assert draw_res.json()["quantity"] == 5
    assert draw_res.json()["stock_status"] == "low_stock"

    # Overdraft drawdown returns 422 client validation error (not 500!)
    over_res = client.post(
        "/api/items/VAC-MRNA99/drawdown",
        json={"units": 999, "reason": "Invalid overdraft"},
    )
    assert over_res.status_code == 422

    # 3. Submit restock order -> Approve -> Fulfill (+15 units -> 20 healthy!)
    restock_res = client.post(
        "/api/restocks",
        json={"sku": "VAC-MRNA99", "order_qty": 15, "requested_by": "Nurse J. Okeke"},
    )
    assert restock_res.status_code == 201
    order_id = restock_res.json()["id"]
    assert restock_res.json()["trace_id"] == restock_res.headers["X-Trace-Id"]

    # Skipping 'approved' directly to 'fulfilled' must fail with 422
    bad_skip = client.patch(
        f"/api/restocks/{order_id}/transition", json={"target_status": "fulfilled"}
    )
    assert bad_skip.status_code == 422

    approve_res = client.patch(
        f"/api/restocks/{order_id}/transition", json={"target_status": "approved"}
    )
    assert approve_res.status_code == 200
    assert approve_res.json()["restock"]["status"] == "approved"

    fulfill_res = client.patch(
        f"/api/restocks/{order_id}/transition", json={"target_status": "fulfilled"}
    )
    assert fulfill_res.status_code == 200
    assert fulfill_res.json()["updated_item"]["quantity"] == 20
    assert fulfill_res.json()["updated_item"]["stock_status"] == "healthy"

    # 4. Verify correlated telemetry signals (Logs + OTel Spans + Prometheus Metrics) & Zero PII
    logs_blob = json.dumps(list(STRUCTURED_LOG_BUFFER))
    assert trace_id in logs_blob
    assert sensitive_email not in logs_blob

    spans = IN_MEMORY_SPAN_EXPORTER.get_finished_spans()
    span_trace_ids = {f"{s.context.trace_id:032x}" for s in spans}
    assert trace_id in span_trace_ids
    for span in spans:
        assert sensitive_email not in json.dumps(dict(span.attributes or {}))

    metrics_res = client.get("/metrics")
    assert metrics_res.status_code == 200
    metrics_text = metrics_res.text
    assert "shelfsync_http_requests_total" in metrics_text
    assert "shelfsync_restock_events_total" in metrics_text
    assert sensitive_email not in metrics_text
