# Product Specification — ShelfSync

* **Public Task Tracker:** [github.com/OmachokoYakubu/ai-dev-tools-zoomcamp/issues](https://github.com/OmachokoYakubu/ai-dev-tools-zoomcamp/issues)
* **API Contract:** [`openapi.yaml`](./openapi.yaml)

---

## 1. Problem Statement

Outpatient clinics, diagnostic labs, and community pharmacies manage temperature-sensitive inventory (vaccines, reagents, sterile kits) across ad-hoc spreadsheets. Two operational failure modes recur daily:
1. **Silent Stockouts:** High-turnover consumables dip below safety thresholds without triggering timely supplier restock orders.
2. **Unverified Restock Fulfillments:** Restock orders are requested by technicians, approved by leads, and received at the dock without an atomic ledger update or audit trail.

**ShelfSync** provides a unified full-stack inventory & restock automation workspace backed by PostgreSQL, end-to-end OpenTelemetry observability, user-impact alerting, and an autonomous self-healing On-Call Responder Agent.

---

## 2. Core User Journey & Acceptance Criteria

### US-1: Real-Time Inventory Catalog & Low-Stock Detection
* **AC-1.1:** Users view all inventory items with SKU, name, category (`cold_chain`, `reagent`, `consumable`), current quantity, reorder threshold, storage temperature, and computed stock status (`healthy`, `low_stock`, `critical_out`).
* **AC-1.2:** Creating a new SKU persists across restarts in PostgreSQL; supplier contact emails (`supplier_email`) are stored safely in the database for ordering but **redacted from all telemetry signals** (`logs`, `spans`, `metrics`).
* **AC-1.3:** Duplicate SKU codes return `HTTP 409 Conflict` without tripping `5xx` error alerts.

### US-2: Stock Drawdown & Automatic Low-Stock Flagging
* **AC-2.1:** Recording a stock consumption (`POST /api/items/{sku}/drawdown`) atomically decrements `quantity` and records an immutable `StockLedgerEvent`.
* **AC-2.2:** Attempting to draw down more units than available in stock returns `HTTP 422 Unprocessable Entity` (client error, isolated from `5xx` user-impact alerts).

### US-3: Multi-Stage Restock Order Lifecycle (Key User Journey)
* **AC-3.1:** Technicians create a restock order (`POST /api/restocks`) for any SKU; the order starts in `requested` status and validates upstream supplier gateway readiness.
* **AC-3.2:** Restock orders follow a strict state machine:
  * `requested` ➔ `approved`
  * `approved` ➔ `fulfilled` (atomically increments item `quantity` by `order_qty` and writes a `restock_fulfilled` ledger entry!)
  * Invalid transitions (e.g., `requested` ➔ `fulfilled` directly, or re-fulfilling an already `fulfilled` order) return `HTTP 422`.

### US-4: Correlated Observability & Zero-PII Telemetry
* **AC-4.1:** Every request on the Restock user journey emits:
  1. **Prometheus Metrics** (`shelfsync_http_requests_total`, `shelfsync_http_request_duration_seconds`, `shelfsync_restock_events_total`),
  2. **OpenTelemetry Distributed Trace Spans** exported via OTLP HTTP to Tempo, and
  3. **Structured JSON Logs** containing the exact `trace_id` and `span_id`, echoed in the `X-Trace-Id` HTTP response header.
* **AC-4.2:** Automated tests assert that `supplier_email` and `Authorization` headers never appear in emitted logs or trace attributes.

### US-5: User-Impact Alerting & Autonomous On-Call Self-Healing
* **AC-5.1:** Prometheus alert rule `ShelfSyncRestockJourneyHigh5xxRate` fires when `5xx` responses on `/api/items` or `/api/restocks` exceed threshold, while ignoring `404`/`422` client mistakes.
* **AC-5.2:** When a bad runtime configuration (`supplier_gateway_mode = "degraded_timeout"`) causes `POST /api/restocks` to fail with `HTTP 503`, the **On-Call Responder Agent** wakes up on the alert webhook (`POST /alerts`), inspects `/ops/diagnostics` & correlated trace error logs, executes bounded rollback (`POST /ops/remediate`), verifies recovery via a synthetic user-journey check, and logs an auditable incident resolution report.
