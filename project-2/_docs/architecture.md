# System Architecture & Observability Design

## 1. Full-Stack & Telemetry Topology

```text
   Browser SPA (Frontend)
         │  HTTP REST + X-Trace-Id
         ▼
  ┌─────────────────────────┐      SQLAlchemy 2.0      ┌────────────────────────┐
  │  ShelfSync FastAPI App  │ ───────────────────────► │  PostgreSQL 16         │
  │  (Port 8080)            │                          │  (items, restocks,     │
  └──────┬─────────┬────────┘                          │   ledger, incidents)   │
         │         │                                   └────────────────────────┘
         │         ├──── OTLP HTTP Spans (:4318) ────► ┌────────────────────────┐
         │         │     (shared trace_id, PII-free)   │  Grafana Tempo         │
         │         │                                   └───────────┬────────────┘
         │         └──── Structured JSON stdout Logs               │
         │               (shared trace_id, redacted)               ▼
         ▼ /metrics                                    ┌────────────────────────┐
  ┌─────────────────────────┐                          │  Grafana UI (:3000)    │
  │  Prometheus (:9090)     │ ───────────────────────► │  Correlated Metrics +  │
  │  + Alert Rules          │                          │  Traces SLO Dashboard  │
  └───────────┬─────────────┘                          └────────────────────────┘
              │ Fires ShelfSyncRestockJourneyHigh5xxRate
              ▼ POST /alerts
  ┌─────────────────────────┐   1. GET /ops/diagnostics
  │  On-Call Responder      │   2. POST /ops/remediate (rollback_supplier_gateway)
  │  Agent (:8081)          │   3. Synthetic Restock Journey Verification
  └─────────────────────────┘
```

## 2. Correlated Signals & PII Boundary
* **Shared Correlation Key:** OpenTelemetry generates a 128-bit `trace_id` per request. Middleware injects `trace_id` and `span_id` into every structured JSON log line, records route-level Prometheus exemplars/counters, and returns `X-Trace-Id` to the client.
* **Redaction Filter:** `backend/telemetry.py` recursively scrubs keys matching `email`, `phone`, `contact`, `password`, `token`, `secret`, `authorization`, and email-formatted substrings before any log record or span attribute leaves the process.
