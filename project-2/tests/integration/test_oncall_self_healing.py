"""Integration test proving autonomous On-Call Responder wake-up & self-healing."""

from __future__ import annotations

import asyncio
import httpx

from backend.main import app
from oncall_agent.responder import AlertItem, triage_and_remediate_alert


def test_oncall_responder_wakes_on_alert_and_fixes_503_outage() -> None:
    async def _scenario() -> None:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://shelfsync-test") as client:
            # 1. Inject degraded supplier gateway fault
            cfg_res = await client.put(
                "/ops/runtime-config",
                json={"supplier_gateway_mode": "degraded_timeout"},
            )
            assert cfg_res.status_code == 200

            # 2. Verify user-impacting failure (HTTP 503) on key restock journey
            failed_restock = await client.post(
                "/api/restocks",
                json={"sku": "VAC-FLU26", "order_qty": 10, "requested_by": "Tech K. Mensah"},
            )
            assert failed_restock.status_code == 503
            failed_trace_id = failed_restock.headers["X-Trace-Id"]

            # 3. Fire user-impact alert to On-Call Responder Agent
            alert = AlertItem(
                status="firing",
                labels={
                    "alertname": "ShelfSyncRestockJourneyHigh5xxRate",
                    "severity": "critical",
                    "service": "shelfsync-app",
                },
                annotations={"summary": "5xx spike on /api/restocks"},
            )
            report = await triage_and_remediate_alert(
                alert, client=client, base_url="http://shelfsync-test"
            )

            assert report["detected_gateway_mode"] == "degraded_timeout"
            assert failed_trace_id in report["correlated_trace_ids"]
            assert report["remediation_applied"] is True
            assert report["action_taken"] == "rollback_supplier_gateway"
            assert report["recovered"] is True

            # 4. Confirm customer restock orders succeed again (HTTP 201)
            recovered_restock = await client.post(
                "/api/restocks",
                json={"sku": "VAC-FLU26", "order_qty": 10, "requested_by": "Tech K. Mensah"},
            )
            assert recovered_restock.status_code == 201

    asyncio.run(_scenario())
