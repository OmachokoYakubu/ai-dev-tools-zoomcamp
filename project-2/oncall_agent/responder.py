"""Autonomous SRE On-Call Responder Agent for ShelfSync.

Wakes up on Prometheus / Alertmanager user-impact alerts, inspects redacted diagnostics
and correlated trace IDs, executes bounded remediation rollbacks, and verifies recovery.
"""

from __future__ import annotations

from datetime import datetime, timezone
import os
from typing import Any

from fastapi import FastAPI
import httpx
from pydantic import BaseModel, Field

from backend.telemetry import redact_pii

APP_BASE_URL = os.getenv("SHELFSYNC_APP_URL", "http://shelfsync-app:8080")
INCIDENT_AUDIT_LOG: list[dict[str, Any]] = []

responder_app = FastAPI(
    title="ShelfSync Autonomous On-Call Responder Agent",
    version="1.0.0",
)


class AlertItem(BaseModel):
    status: str = "firing"
    labels: dict[str, str] = Field(default_factory=dict)
    annotations: dict[str, str] = Field(default_factory=dict)


class AlertWebhookPayload(BaseModel):
    alerts: list[AlertItem] = Field(default_factory=list)


async def triage_and_remediate_alert(
    alert: AlertItem,
    client: httpx.AsyncClient,
    base_url: str = APP_BASE_URL,
) -> dict[str, Any]:
    alertname = alert.labels.get("alertname", "UnknownAlert")
    if alert.status == "resolved":
        return {"alertname": alertname, "status": "ignored_resolved", "action": "none"}

    if alert.labels.get("test") == "true":
        return {
            "alertname": alertname,
            "status": "handled_synthetic_ping",
            "action": "verified_responder_online",
        }

    # Step 1: Bounded read-only diagnostic inspection
    diag_res = await client.get(f"{base_url}/ops/diagnostics", timeout=10.0)
    diag_res.raise_for_status()
    diag = diag_res.json()

    runtime_cfg = diag.get("runtime_config", {})
    gateway_mode = runtime_cfg.get("supplier_gateway_mode", "healthy")
    error_traces = diag.get("recent_5xx_traces", [])
    correlated_trace_ids = [
        entry.get("trace_id") for entry in error_traces if entry.get("trace_id")
    ]

    remediation_applied = False
    action_taken = "no_config_drift_detected"

    # Step 2: Autonomous root-cause remediation if gateway config drifted
    if gateway_mode != "healthy":
        rem_res = await client.post(
            f"{base_url}/ops/remediate",
            json={
                "action": "rollback_supplier_gateway",
                "triggered_by": "oncall-responder-agent",
                "reason": f"Auto-remediation for firing alert {alertname} (mode={gateway_mode})",
            },
            timeout=10.0,
        )
        rem_res.raise_for_status()
        remediation_applied = True
        action_taken = "rollback_supplier_gateway"

    # Step 3: Post-remediation user-journey verification probe
    health_res = await client.get(f"{base_url}/healthz", timeout=10.0)
    probe_res = await client.post(
        f"{base_url}/api/restocks",
        json={
            "sku": "VAC-FLU26",
            "order_qty": 5,
            "requested_by": "oncall-synthetic-verifier",
        },
        timeout=10.0,
    )
    recovered = health_res.status_code == 200 and probe_res.status_code == 201

    incident_record = redact_pii(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "alertname": alertname,
            "severity": alert.labels.get("severity", "critical"),
            "detected_gateway_mode": gateway_mode,
            "correlated_trace_ids": correlated_trace_ids[-5:],
            "remediation_applied": remediation_applied,
            "action_taken": action_taken,
            "post_fix_journey_status": probe_res.status_code,
            "verification_trace_id": probe_res.headers.get("X-Trace-Id", ""),
            "recovered": recovered,
        }
    )
    INCIDENT_AUDIT_LOG.append(incident_record)
    return incident_record


@responder_app.get("/healthz")
def responder_health() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "shelfsync-oncall-responder",
        "incidents_handled": len(INCIDENT_AUDIT_LOG),
    }


@responder_app.get("/incidents")
def list_incidents() -> list[dict[str, Any]]:
    return list(INCIDENT_AUDIT_LOG)


@responder_app.post("/alerts")
async def receive_alerts(payload: AlertWebhookPayload) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    async with httpx.AsyncClient() as client:
        for alert in payload.alerts:
            outcome = await triage_and_remediate_alert(
                alert, client=client, base_url=APP_BASE_URL
            )
            results.append(outcome)
    return {
        "status": "processed",
        "count": len(results),
        "results": results,
    }
