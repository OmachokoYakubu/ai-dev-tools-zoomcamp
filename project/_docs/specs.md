# Product Specification: Order Tracker & Auto-Remediation System

* **Project:** Order Tracker & Incident Responder (Flagship Capstone)
* **Author:** Omachoko Yakubu
* **Course:** DataTalks.Club AI Dev Tools Zoomcamp 2026

---

## 1. Executive Summary & Problem Statement

Modern e-commerce and logistics platforms face high operational costs when customer-facing status endpoints fail silently or return erroneous delivery projections. Customers experience anxiety, customer support queues inflate rapidly, and manual diagnosis across siloed logs and distributed servers requires significant engineering time.

**Order Tracker** is an end-to-end, resilient order management and tracking platform built with an automated telemetry loop and an autonomous on-call incident response agent. It provides customers with deterministic order tracking, guarantees delivery estimations across calendar month boundaries, and automatically detects, isolates, and remediates 5xx server errors without human intervention.

---

## 2. User Stories & Acceptance Criteria

### US-1: Customer Order Status Lookup
* **As a** customer,
* **I want to** check the current status and estimated delivery date of my order by entering its Order ID,
* **So that** I know when to expect my package.
* **Acceptance Criteria:**
  - `GET /api/orders/{id}` returns HTTP 200 with `{id, customer, item, priority, status, created_at}`.
  - If `priority == "express"`, the response includes a calculated `estimated_delivery` date exactly 2 days after creation.
  - The delivery date calculation must accurately handle calendar month and year transitions (e.g. March 31 + 2 days = April 2).
  - If the order ID does not exist, return HTTP 404 with `{"detail": "Order not found"}`.

### US-2: Order Placement and Lifecycle Updates
* **As a** merchant or fulfillment worker,
* **I want to** submit new customer orders and advance their status from `received` to `preparing`, `shipped`, and `delivered`,
* **So that** customer tracking reflects real fulfillment progress.
* **Acceptance Criteria:**
  - `POST /api/orders` accepts `{customer, item, priority}` and returns HTTP 201 with a unique order ID.
  - `PATCH /api/orders/{id}` accepts `{status}` (valid values: `received`, `preparing`, `shipped`, `delivered`) and returns HTTP 200 with updated order record.
  - Invalid status returns HTTP 422 Unprocessable Entity.

### US-3: System Health & Persistent Storage
* **As an** SRE / DevOps engineer,
* **I want** deterministic health checks and durable persistence,
* **So that** container restarts do not drop in-flight order states.
* **Acceptance Criteria:**
  - `GET /healthz` queries the live SQLite database (`SELECT 1`) and returns `{"status": "ok"}`.
  - Database is stored in a dedicated volume (`/data/orders.db`) persisting across container recreation.

### US-4: User-Impact Observability & Alerting
* **As an** Operations Lead,
* **I want** real-time metrics, traces, and automated alerts on user-impacting errors,
* **So that** degraded customer experience is caught immediately.
* **Acceptance Criteria:**
  - Every HTTP request generates structured logs and metrics tagged with request method, path, and HTTP status code.
  - User-impacting 5xx errors fire an automated webhook alert within 60 seconds.
  - Client-side 404 errors (e.g., misspelled order IDs) do not trigger operational alerts.

### US-5: Autonomous Incident Responder
* **As an** on-call engineer,
* **I want** an autonomous responder agent to triage webhook alerts,
* **So that** known defects are investigated and resolved with zero manual intervention.
* **Acceptance Criteria:**
  - On-call agent listens on `POST /alerts`.
  - Analyzes incoming alert payload, identifies affected route and error trace.
  - Verifies whether the alert is synthetic/test or an active regression.
  - Dispatches automated diagnostic report and applies root-cause remediation.
