# Incident Response Runbook — ShelfSync On-Call Agent

## Alert: `ShelfSyncRestockJourneyHigh5xxRate`
* **Severity:** `critical` (Direct User Impact — technicians blocked from submitting restock orders)
* **Condition:** `5xx` error rate on `/api/restocks` or `/api/items` exceeds `5%` over `1m` window (`404` and `422` client errors are excluded).

### Automated Responder Protocol (`oncall_agent/responder.py`)
1. **Ingest Webhook:** Parse firing alert labels (`alertname`, `severity`, `service`) from Prometheus / Alertmanager (`POST /alerts`).
2. **Bounded Read-Only Triage:** Query `GET /ops/diagnostics` on `shelfsync-app` to inspect:
   * Current `runtime_config` (`supplier_gateway_mode`),
   * Recent `5xx` structured error ring-buffer entries with `trace_id` (PII-redacted), and
   * Database connectivity status.
3. **Root-Cause Remediation:**
   * If `supplier_gateway_mode != "healthy"`, invoke `POST /ops/remediate` with `{"action": "rollback_supplier_gateway", "triggered_by": "oncall-responder-agent"}` to restore known-good configuration.
4. **Post-Fix Verification:** Execute a live synthetic probe against `/healthz` and `GET /api/restocks` (plus verify `supplier_gateway_mode == "healthy"`), confirming HTTP `200` recovery.
5. **Audit Record:** Persist a structured incident report containing alert metadata, correlated `trace_id`s, remediation action taken, and recovery verification status (`GET /incidents`).
