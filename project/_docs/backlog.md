# Task Tracker & Execution Backlog

This document acts as the public task tracker for the Order Tracker project, showing acceptance criteria, assigned agents, and execution history.

---

## 📊 Sprint Board

| Task ID | Title | Assigned Agent | Status | Acceptance Criteria Met |
| :--- | :--- | :--- | :--- | :--- |
| **TSK-01** | Full-Stack FastAPI & Web UI Setup | `Agent-Backend` | ✅ Done | REST endpoints for CRUD + single-page client interface |
| **TSK-02** | SQLite Persistence & Docker Volume Seam | `Agent-DevOps` | ✅ Done | Docker Compose mounts `/data/orders.db` volume surviving restarts |
| **TSK-03** | Automated Test Suite (Unit & Integration) | `Agent-QA` | ✅ Done | Pytest coverage for health, orders, 404 handling, month-boundary math |
| **TSK-04** | OpenTelemetry, Prometheus & Grafana Stack | `Agent-SRE` | ✅ Done | Metrics collection, Prometheus scraping, Grafana dashboards |
| **TSK-05** | User-Impact Alert Rules (5xx vs 4xx Isolation) | `Agent-SRE` | ✅ Done | Alert rule triggers only on persistent 5xx server errors |
| **TSK-06** | Autonomous On-Call Incident Responder | `Agent-OnCall` | ✅ Done | Webhook listener triages alerts, parses traces, and executes runbook |
| **TSK-07** | Month-End Boundary Bug Fix & Regression Test | `Agent-Backend` | ✅ Done | Replaced `.replace(day=...)` with `timedelta(days=2)`, verified via test |
| **TSK-08** | CI/CD GitHub Actions Workflow Integration | `Agent-DevOps` | ✅ Done | Automated pytest execution and container build verification on push/PR |

---

## 📝 Detailed Task Specifications & Agent Execution Logs

### TSK-01: Full-Stack Application Scaffold
* **Owner:** `Agent-Backend`
* **Deliverables:** `app/main.py`, `static/index.html`
* **Agent Log:**
  > Implemented FastAPI service with `/api/orders`, `/healthz`, and static asset mounting. Configured Pydantic schemas for `NewOrder` and `StatusUpdate`. Validated against CORS and standard HTTP response codes.

### TSK-02: Containerization & Persistent Volume
* **Owner:** `Agent-DevOps`
* **Deliverables:** `Dockerfile`, `compose.yaml`
* **Agent Log:**
  > Multi-stage Dockerfile built on `python:3.11-slim`. Configured `compose.yaml` with named volume `orders:/data`. Tested container recreation with `docker compose down && docker compose up -d` — verified all 3 seeded records remain intact.

### TSK-03: Automated Test Suite
* **Owner:** `Agent-QA`
* **Deliverables:** `tests/test_api.py`, `tests/test_incident_response.py`
* **Agent Log:**
  > Created fixture with temporary SQLite file using monkeypatching. Built 5 test cases checking health checks, order creation, status transitions, missing ID 404 responses, and date boundary calculations. All 5 tests passed in 1.88s.

### TSK-04: Observability Pipeline
* **Owner:** `Agent-SRE`
* **Deliverables:** `telemetry/dashboard.json`, Prometheus configuration
* **Agent Log:**
  > Instrumented FastAPI middleware to capture request durations, status code counts, and active connections. Configured OpenTelemetry tracing headers forwarding trace IDs to client responses.

### TSK-05: Alerting on Real User Impact
* **Owner:** `Agent-SRE`
* **Deliverables:** `telemetry/alerts.yml`
* **Agent Log:**
  > Configured Alertmanager rule `HighErrorRate5xx` with expression `rate(http_requests_total{status=~"5.."}[1m]) > 0`. Confirmed that 404 requests from non-existent order lookups do not trip the threshold.

### TSK-06: Autonomous Incident Responder
* **Owner:** `Agent-OnCall`
* **Deliverables:** `incident-response/responder.py`, `incident-response/runbook.md`
* **Agent Log:**
  > Developed webhook server listening on port 8001. Handles incoming Grafana/Alertmanager payloads. Implemented synthetic test filter (`ResponderTest`) and automatic trace capture.

### TSK-07: Root-Cause Investigation & Fix (Express Delivery Boundary Bug)
* **Owner:** `Agent-Backend`
* **Deliverables:** `app/main.py:58-60`, regression test case
* **Agent Log:**
  > Investigated 500 error triggered by `GET /api/orders/express-1002`. Found `placed_at.replace(day=placed_at.day + 2)` raised `ValueError` when order created at month end. Fixed using `placed_at + timedelta(days=2)`. Added regression test `test_express_order_delivery_calculation`.
